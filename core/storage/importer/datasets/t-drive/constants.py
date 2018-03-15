
# -------------------- Redis constants -------------------------------------- #
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# -------------------- Elasticsearch constants ------------------------------ #

# basic configuration
ELASTICSEARCH_HOST = 'localhost'
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

