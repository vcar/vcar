import redis
import csv
import copy
import json
from time import strftime, sleep
from elasticsearch import Elasticsearch, helpers
from .constants import *

# ----------------- Setting up tools  --------------------------------------- #
red = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB
)


def task_info(name='info'):
    p = red.pubsub(ignore_subscribe_messages=True)
    p.subscribe(name)
    thread = p.run_in_thread(sleep_time=0.001)
    # thread.stop()

# def task_info(name='info'):
#     pubsub = red.pubsub()
#     pubsub.subscribe(name)
#     for message in pubsub.listen():
#         # print("[+] Message: {}".format(message))
#         yield 'data: {}\n\n'.format(message['data'])

# ----------------- Indexing with Bulk : Large files  ----------------------- #


def index_bulk(traces, dataset, user_id, bulk_size=BULK_SIZE):
    try:
        es = Elasticsearch([{
            'host': ELASTICSEARCH_HOST,
            'port': ELASTICSEARCH_PORT
        }])

        index = dataset.slug
        type = "dataset"
        es.cluster.health(wait_for_status='yellow', request_timeout=30)
        mapping = {
            type: {
                "properties": {
                    "user": {
                        "type": "integer"
                    },
                    "vehicle": {
                        "type": "integer"
                    },
                    "driver": {
                        "type": "integer"
                    },
                    "class": {
                        "type": "string"
                    },
                    "name": {
                        "type": "string",
                                "index": "not_analyzed"
                    },
                    "value": {
                        "type": "string",
                                "index": "not_analyzed"
                    },
                    "timestamp": {
                        "type": "date",
                        "format": "yyyy-MM-dd HH:mm:ss"
                    }
                }
            }
        }

        if not es.indices.exists(index=index):
            es.indices.create(index=index, ignore=400)
            es.indices.put_mapping(index=index, doc_type=type, body=mapping)

        for trace in traces:
            actions = []
            i = 1
            ignored = 0
            with open(trace, 'r') as f:
                reader = csv.reader(f)
                for line in reader:
                    try:
                        vehicle = int(line[0])
                        driver = int(line[0])
                        lat = float(line[2])
                        lng = float(line[3])
                        timestamp = line[1]
                        # adding Latitude
                        actions.append({
                            "_index": dataset.slug,
                            "_type": 'dataset',
                            "_source": {
                                "user": user_id,
                                "vehicle": vehicle,
                                "driver": driver,
                                "class": 3,
                                "name": 'latitude',
                                "value": lat,
                                "timestamp": timestamp
                            }
                        })
                        # adding Longitude
                        actions.append({
                            "_index": dataset.slug,
                            "_type": 'dataset',
                            "_source": {
                                "user": user_id,
                                "vehicle": vehicle,
                                "driver": driver,
                                "class": 3,
                                "name": 'longitude',
                                "value": lng,
                                "timestamp": timestamp
                            }
                        })
                        if i*2 % bulk_size == 0:
                            helpers.bulk(es, actions)
                            actions = []
                            print(" ============================================> Bulk : i = " + str(i))
                        i += 1
                    except:
                        ignored += 1
            if i < bulk_size:
                print(" ============================================> Bulk Rest : i = " + str(i))
                helpers.bulk(es, actions)
        # bulk the actions dict to elastic
        helpers.bulk(es, actions)
        # End processing files
        if ignored > 0:
            red.publish('info', 'background indexing completed with {} ignored line(s)'.format(ignored))
        else:
            red.publish('info', 'Background indexing task [<b>{}</b> file<small>(s)</small>] completed successfully.'.format(len(traces)))
        return True
        sys.exit()
    except Exception as e:
        print('Exception OUT: ', e)
        red.publish('info', 'Exception: {}'.format(e))
        return False
        sys.exit()
