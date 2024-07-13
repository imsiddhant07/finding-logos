import json


class JSONDumpingService(object):
    """A service class for dumping a JSON object to a file."""
    def __init__(self):
        super().__init__()
        
    def get(self, **kwargs):
        """Dumps the provided json_object to json_path with formatted indentation.

        Args:
        - json_path (str): File path where JSON will be dumped.
        - json_object (Any): JSON object to be dumped.

        Raises:
            IOError: If there is an issue writing to json_path.
        """
        json_path = kwargs.get('json_path')
        json_object = kwargs.get('json_object')
        
        with open(json_path, 'w') as f:
            json.dump(json_object, f, indent=4)
