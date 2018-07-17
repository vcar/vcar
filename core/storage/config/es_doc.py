MAPPING = {
    "row": { # document type :: row || transformed
        "properties": {
            # main signals
            "name": {
                "type": "string",
            },
            "value": { # are always string with meta value_type
                "type": "string",
            },
            # metadata
            # _id : already included
            "dataset":      {"type": "string"},
            "event":        {"type": "integer"},
            "timestamp":    {"type": "date"}
            "user":         {"type": "integer"},
            "vehicle":      {"type": "integer"},
            "driver":       {"type": "integer"},
            "source":       {"type": "string"},
            "class":        {"type": "string"},

            "value_type":   {"type": "string"}, # for custing purposes
        }
    }
}