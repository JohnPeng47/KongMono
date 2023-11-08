import json

with open("../settings.json") as settings_file:
    settings = json.loads(settings_file.read())

db_host = settings["db_host"]
db_port = settings["db_port"]
