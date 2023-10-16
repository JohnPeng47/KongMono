GENERATE_SECTION_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string"
            },
            "section": {
                "type": "string"
            },
            "keywords": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["name", "section", "keywords"]
    }
}


EXPAND_TEXT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "expansion": {"type": "string"},
            "section": {"type": "string"},
            "keywords": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["expansion", "section", "keywords"]
    }
}


EXPAND_SUBTREE_DETAILS = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "additionalProperties": {
        "type": "string"
    }
}