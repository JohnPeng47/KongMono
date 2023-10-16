import json
import jsonschema

from typing import List
import csv
import yaml

def equal(obj1, obj2, ignore_order=False):
    # Remove "id" fields from both objects and sort lists if ignore_order is True
    remove_id_fields(obj1, ignore_order)
    remove_id_fields(obj2, ignore_order)

    # Convert back to JSON strings for comparison
    cleaned_json1 = json.dumps(obj1, sort_keys=True)
    cleaned_json2 = json.dumps(obj2, sort_keys=True)

    print(cleaned_json1)
    print(cleaned_json2)

    # Compare the cleaned JSON strings
    return cleaned_json1 == cleaned_json2

def remove_id_fields(obj, ignore_order):
    if isinstance(obj, dict):
        # Remove "id" field if present
        obj.pop("id", None)
        # Remove mongo id
        obj.pop("_id", None)
        # Recursively remove "id" fields from nested dictionaries
        for value in obj.values():
            remove_id_fields(value, ignore_order)
            
    elif isinstance(obj, list):
        # Recursively remove "id" fields from nested lists
        for item in obj:
            remove_id_fields(item, ignore_order)
        # If ignore_order is True, sort the list
        if ignore_order:
            try:
                obj.sort()
            except TypeError:
                # In case of a list with unsortable elements (dicts, lists), 
                # we convert each element into json string and then sort
                obj.sort(key=lambda x: json.dumps(x, sort_keys=True))

def validate_schema(data, schema):
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        return False
    return True

def is_csv_files_equal(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        csv_reader1 = csv.reader(file1)
        csv_reader2 = csv.reader(file2)

        for row1, row2 in zip(csv_reader1, csv_reader2):
            if row1 != row2:
                return False

        # Check if one file has more rows than the other
        for _ in csv_reader1:
            return False
        for _ in csv_reader2:
            return False

    return True

def is_yaml_files_equal(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        data1 = yaml.safe_load(file1)
        data2 = yaml.safe_load(file2)

    return data1 == data2
