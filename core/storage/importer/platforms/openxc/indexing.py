import redis
import json
from time import strftime, sleep
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
from .constants import *
from .helpers import correct_value, correct_time
from ...transformer import Transformer

# ----------------- Setting up tools  --------------------------------------- #
red = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB
)


def my_handler(message):
    # print('MY HANDLER: {}'.format(message['data']))
    yield 'data: {}\n\n'.format(message['data'])


def task_info(name='info'):
    p = red.pubsub(ignore_subscribe_messages=True)
    p.subscribe('info')
    # p.subscribe(**{'info': msg_handler})
    # thread = p.run_in_thread(sleep_time=0.001)
    # thread.stop()
    while True:
        msg = p.get_message()
        if msg:
            yield 'data: {}\n\n'.format(msg['data'])
        sleep(1)

    # pubsub = red.pubsub()
    # pubsub.subscribe(name)
    # for message in pubsub.listen():
    #     # print("[+] Message: {}".format(message))
    #     yield 'data: {}\n\n'.format(message['data'])

# ----------------- Indexing with Bulk : Large files  ----------------------- #


def index_bulk(traces, metadata, bulk_size=BULK_SIZE):
    red.publish('info', 'Hello word! ')
    try:
        es = Elasticsearch([{
            'host': ELASTICSEARCH_HOST,
            'port': ELASTICSEARCH_PORT
        }])

        index = OPENXC_INDEX
        type = "platform"
        es.cluster.health(wait_for_status='yellow', request_timeout=30)

        # es.indices.delete(index=index, ignore=404)
        if not es.indices.exists(index=index):
            es.indices.create(index=index, ignore=400)
            es.indices.put_mapping(index=index, doc_type=type, body=MAPPING)

        # inisialise a Transformer instance + set the platform attribute
        tr = Transformer()
        tr.setPlatformById(metadata['platform'])

        for trace in traces:
            i = 1
            actions = []
            with open(trace, 'r') as f:
                for line in f:
                    source = json.loads(line)
                    signal = tr.getInfo(source.get('name'))

                    if signal is not None:
                        action = {
                            "_index": index,
                            "_type": type,
                            "_id": i,
                            "_source": {
                                "user": metadata['user'],
                                "vehicle": metadata['vehicle'],
                                "driver": metadata['driver'],
                                "class": signal['class'],
                                "name": signal['name'],
                                "value": source.get('value'),
                                "timestamp": correct_time(source.get('timestamp'))
                            }
                        }
                        actions.append(action)
                        if i % bulk_size == 0:
                            helpers.bulk(es, actions)
                            actions = []
                        i += 1
                    else:
                        """ Signal not included, should we remove it !! """
                        pass

            if i < bulk_size:
                helpers.bulk(es, actions)
        red.publish(
            'info', 'Background indexing task [<b>{}</b> file<small>(s)</small>] has been completed successfully.'.format(len(traces)))
        # sleep(1)
        # red.connection_pool.disconnect()
        return True
        sys.exit()
    except Exception as e:
        print('Exception: ', e)
        red.publish('info', 'Exception: {}'.format(e))
        return False
        sys.exit()
