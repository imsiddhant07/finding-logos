import json


class JSONDumpingService(object):
    def __init__(self):
        super().__init__()
        
    def get(self, **kwargs):
        json_path = kwargs.get('json_path')
        json_object = kwargs.get('json_object')
        
        with open(json_path, 'w') as f:
            json.dump(json_object, f, indent=4)
