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
	host = REDIS_HOST,
	port = REDIS_PORT,
	db = REDIS_DB
)

def task_info(name='info'):
    pubsub = red.pubsub()
    pubsub.subscribe(name)
    for message in pubsub.listen():
        # print("[+] Message: {}".format(message))
        yield 'data: {}\n\n'.format(message['data'])

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
		sleep(2)
		red.publish('info', 'Inisializing Elasticsearch ...')
		es.cluster.health(wait_for_status='yellow', request_timeout=30)
		red.publish('info', 'creating index if it dosn\'t exist ...')
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

		# inisialise a Transformer instance + set the platform attribute
		tr = Transformer();
		tr.setPlatformById(metadata['platform']);
		for trace in traces:
			i = 1
			red.publish('info', 'indexing the file: {}'.format(trace))
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
							red.publish('info', '{} events indexed'.format(i))
							actions = []
						i += 1
					else:
						""" Signal not included, should we remove it !! """
						pass

					# ,overwrite_existing=True
					# es.index(index=index, doc_type=type, id=i, body=line)
			if i < bulk_size:
				helpers.bulk(es, actions)
			red.publish('info', 'File {} indexed'.format(trace))
			red.publish('info', 'end_trace'.format(trace))
		red.publish('info', 'end_all')
		sleep(2)
		red.connection_pool.disconnect()
		return True
		sys.exit()
	except Exception as e:
		print('Exception: ', e)
		red.publish('info', 'Exception: {}'.format(e))
		return False
		sys.exit()
