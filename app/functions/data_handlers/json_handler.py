import json
from importlib.resources import files
from ..config import config_path

def save_to_json():
    dict = {
        "channel name": "",
        "database name": "",
        "max search depth": "2",
    }
    with open(config_path, "w")  as f:
        json.dump(dict, f)

def modify_max_depth_search(new):
    with open(config_path) as f:
        dict = json.load(f)
    
    dict["max search depth"] = new

    with open(config_path, "w")  as f:
        json.dump(dict, f)

def modify_channel_name(new):
    with open(config_path) as f:
        dict = json.load(f)
    
    dict["channel name"] = new

    with open(config_path, "w")  as f:
        json.dump(dict, f)

def modify_database_name(new):
    with open(config_path) as f:
        dict = json.load(f)
    
    dict["database name"] = new

    with open(config_path, "w")  as f:
        json.dump(dict, f)


def fetch_max_depth_search():
    with open(config_path) as f:
        dict = json.load(f)
        return dict["max search depth"]

def fetch_channel_name():
    with open(config_path) as f:
        dict = json.load(f)
        return dict["channel name"]
    
def fetch_database_name():
    with open(config_path) as f:
        dict = json.load(f)
        return dict["database name"]




