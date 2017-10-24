from elasticsearch import Elasticsearch, helpers

es = Elasticsearch()
index = "openxc"
type = "driver_1"
es.cluster.health(wait_for_status='yellow', request_timeout=1)
# count documents
# count = es.count(index=index, doc_type=type)
# print(count)
# get one document
# data = es.get(index=index, doc_type=type, id=200)
# print(data)
# search one signal
body = {
    "query": {
        "match": {
            'name': 'accelerator_pedal_position'
        }
    }
}
# search = es.search(index=index, doc_type=type, body=body, _source=False)

# print(search)

# Query for all results (no matching criteria)
# res = es.search(index=index, body={"query": {"match_all": {}}})
# print (res['hits']['total'])
# print (res['hits']['hits'][100]['_source']['name'])

# bulk
body = {
    '_op_type': 'delete',  # values are (index, create, delete, update)
    '_index': 'index-name',
    '_type': 'document',
    '_id': 42,
}

# if not es.exists(index=index, doc_type=type):
#     print("NOOOO")
# if es.exists(index=index, doc_type=type):
#     print("YEEES")
# Mapping

mapping = {
    type: {
        "properties": {
            "name": {
                "type": "string"
            },
            "value": {
                "type": "double"
            },
            "timestamp": {
                "type": "date",
                "format": "epoch_millis"
            }
        }
    }
}
# if not es.indices.exists(index=index):
#     es.indices.create(index=index, ignore=400)
#     es.indices.put_mapping(index=index, doc_type=type, body=mapping)
#     x = "1364323978.53600"
#     t = x.split('.')
#     data = {
#         "name": "accelerator_pedal_position",
#         "timestamp": '{}{}'.format(t[0], t[1][:3]),
#         "value": 53.5
#     }
#     es.index(index=index, doc_type=type, id=1, body=data)
#     print("index creared")
# else:
#     es.indices.delete(index=index, ignore=404)


def correct_time(timestamp):
    try:
        timestamp = str(timestamp)
        print(timestamp)
        t = timestamp.split('.')
        return '{}{}'.format(t[0], t[1][:3].ljust(3, '0'))
    except:
        return timestamp.split('.')[0]

x = correct_time(1361454774.657980)
print(x)
# 13614547982
# 136145482189
# 136145484557
# 136145486924
# 136145489296
# 136145491667
# 136145494043
# 136145496416
# 136145498789
# 13614550116
# 13614550353
# 136145505902

# put_mapping(*args, **kwargs)
# http://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.client.IndicesClient.put_mapping
# https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-put-mapping.html
mapping = '''
    {
      "mappings":{
        "logs_june":{
          "_timestamp":{
            "enabled":"true"
          },
          "properties":{
            "logdate":{
              "type":"date",
              "format":"dd/MM/yyy HH:mm:ss"
            }
          }
        }
      }
    }
'''
# self.elastic_con.indices.create(index='test-index', ignore=400, body=mapping)
# 2
# conntect es
# es = Elasticsearch()
# delete index if exists
# if es.indices.exists(config.elastic_urls_index):
#     es.indices.delete(index=config.elastic_urls_index)
# index settings
settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "urls": {
            "properties": {
                "url": {
                    "type": "string"
                }
            }
        }
    }
}
# create index
# es.indices.create(index=config.elastic_urls_index, ignore=400, body=settings)

# Notes
# curl -XGET 'http://localhost:9200/openxc/driver_1/1/_source'
# curl --head 'http://localhost:9200/openxc/driver_1/1/_source'
# curl -XGET 'http://localhost:9200/openxc/driver_1/1?fields=name,value'
# curl -XGET 'http://localhost:9200/openxc/driver_1/1?_source=false'
# curl -XGET 'http://localhost:9200/openxc/driver_1/_search?pretty&q=name:vehicle_speed'
# curl -XGET 'http://localhost:9200/openxc/driver_1/_search?pretty&size=10000'

{
  "size": 0,
  "aggs": {
    "2": {
      "date_histogram": {
        "field": "timestamp",
        "interval": "1s",
        "time_zone": "Europe/London",
        "min_doc_count": 1,
        "extended_bounds": {
          "min": 1361454733109,
          "max": 1361454981775
        }
      },
      "aggs": {
        "1": {
          "max": {
            "field": "value"
          }
        }
      }
    }
  },
  "highlight": {
    "pre_tags": [
      "@kibana-highlighted-field@"
    ],
    "post_tags": [
      "@/kibana-highlighted-field@"
    ],
    "fields": {
      "*": {}
    },
    "require_field_match": false,
    "fragment_size": 2147483647
  },
  "query": {
    "filtered": {
      "query": {
        "query_string": {
          "analyze_wildcard": true,
          "query": "*name=\"vehicle_speed\""
        }
      },
      "filter": {
        "bool": {
          "must": [
            {
              "range": {
                "timestamp": {
                  "gte": 1361454733109,
                  "lte": 1361454981775,
                  "format": "epoch_millis"
                }
              }
            }
          ],
          "must_not": []
        }
      }
    }
  }
}
