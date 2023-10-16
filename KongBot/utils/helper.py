from itertools import islice
from typing import Dict
import json
from bson import ObjectId
import uuid
import tiktoken

def get_nth(iterator, index):
    "Return the nth item or a default value"
    try:
        return next(islice(iterator, index, None))
    except StopIteration:
        return None  # Or any default value
    

def double_encode_json(json_data: Dict):
    import json
    
    json_str = json.dumps(json_data)
    json_str.replace("{", "{{")
    json_str.replace("}", "}}")
    return json_str

def gen_unique_id():
    return str(uuid.uuid4())


def gen_unique_runid():
    return "run-id::" + str(uuid.uuid4())

def print_mongo(obj: Dict):
    class MongoDBJSONEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, ObjectId):
                return str(obj)
            return json.JSONEncoder.default(self, obj)

    print(json.dumps(obj, indent=4, cls=MongoDBJSONEncoder))


def count_json_objects(json_data):
    if isinstance(json_data, dict):
        count = 1
        for key, value in json_data.items():
            count += count_json_objects(value)
        return count
    elif isinstance(json_data, list):
        count = 0
        for item in json_data:
            count += count_json_objects(item)
        return count
    else:
        return 1
    
def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """
    Returns the number of tokens in a text string
    """
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens