import redis
import json
from time import strftime, sleep
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
from .constants import BULK_SIZE
from .helpers import correct_value, correct_time
red = redis.StrictRedis(host='localhost', port=6379, db=0)


def task_info(name='info'):
    pubsub = red.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe(name)
    for message in pubsub.listen():
        # print("[+] Message: {}".format(message))
        yield 'data: {}\n\n'.format(message['data'])
# ---------------------------- Process openxc task -------------------------- #


def openxc_task(traces, user_id):
    try:
        es = Elasticsearch([{
            'host': 'localhost',
            'port': 9200
        }])
        index = "openxc"
        type = "driver_{}".format(user_id)
        sleep(2)
        red.publish('info', 'Inisializing Elasticsearch ...')
        es.cluster.health(wait_for_status='yellow', request_timeout=1)

        red.publish('info', 'creating index if it dosn\'t exist ...')
        mapping = {
            type: {
                "properties": {
                    "name": {
                        "type": "string",
                        "index":    "not_analyzed"
                    },
                    "value": {
                        "type": "string",
                        "index":    "not_analyzed"
                    },
                    "timestamp": {
                        "type": "date"
                    }
                }
            }
        }
        # es.indices.delete(index=index, ignore=404)
        if not es.indices.exists(index=index):
            es.indices.create(index=index, ignore=400)
            es.indices.put_mapping(index=index, doc_type=type, body=mapping)

        for trace in traces:
            i = 1
            red.publish('info', 'indexing the file: {}'.format(trace))
            actions = []
            with open(trace, 'r') as f:
                for line in f:
                    source = json.loads(line)
                    action = {
                        "_index": index,
                        "_type": type,
                        "_id": i,
                        "_source": {
                            "name": source.get('name'),
                            # "value": correct_value(source.get('value')),
                            "value": source.get('value'),
                            "timestamp": correct_time(source.get('timestamp'))
                        }
                    }
                    actions.append(action)
                    if i % BULK_SIZE == 0:
                        helpers.bulk(es, actions)
                        red.publish('info', '{} events indexed'.format(i))
                        actions = []
                    i += 1
                    # ,overwrite_existing=True
                    # es.index(index=index, doc_type=type, id=i, body=line)
            if i < BULK_SIZE:
                helpers.bulk(es, actions)
            red.publish('info', 'File {} indexed'.format(trace))
            red.publish('info', 'end_trace'.format(trace))
        red.publish('info', 'end_all')
        print('[+] DONE ALL FILES')
        red.publish('info', 'end_all')
        red.connection_pool.disconnect()
        return True
        sys.exit()
    except Exception as e:
        print('Exception: ', e)
        red.publish('info', 'Exception: {}'.format(e))
        return False
        sys.exit()


# def realtime_info(info=None):
#     socketio.emit(
#         'send_info',
#         {
#             'data': info.get('data', 'No data!'),
#             'status': info.get('status', 'GREEN')
#         },
#         namespace='/import'
#     )
