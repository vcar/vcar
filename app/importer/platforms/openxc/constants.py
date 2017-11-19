
# -------------------- Redis constants -------------------------------------- #
REDIS_HOST = 'localhost'  # default config when runing inside a virtualenv
# REDIS_HOST = 'redis'  # docker links
REDIS_PORT = 6379
REDIS_DB = 1

# -------------------- Elasticsearch constants ------------------------------ #

# basic configuration
# ELASTICSEARCH_HOST = 'localhost' # default config when runing inside a virtualenv
ELASTICSEARCH_HOST = 'elastic'  # docker links
ELASTICSEARCH_PORT = 9200

# indexing configuration
OPENXC_INDEX = 'openxc'
BULK_SIZE = 10000

# -------------------- Driver Graph Configuration --------------------------- #
TRANSFORM = {
    -1: "reverse",
    0: "neutral",
    1: "first",
    2: "second",
    3: "third",
    4: "fourth",
    5: "fifth",
    6: "sixth",
    7: "seventh"
}

MAPPING = {
    "platform": {
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
                "type": "date"
            }
        }
    }
}
