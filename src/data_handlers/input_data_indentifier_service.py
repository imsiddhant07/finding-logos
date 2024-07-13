import os
from urllib.parse import urlparse
from src.data_handlers.constants import DataSources

class DataSourceIdentifierService(object):
    """A class to identify data sources."""
    def __init__(self):
        super().__init__()
    
    def get(self, **kwargs):
        """Method to determine input type.
        
        Args:
        ** kwargs: Arbitary keyword arguments.
        - data_source (str): data source path.

        Returns:
        - DataSources: returns either of DataSources object
        """
        # Step 1: Declarations
        data_source = kwargs.get('data_source')
        parsed = urlparse(data_source)
        
        # Step 2: Check if it has a scheme and netloc (like 'http', 'https' in URLs)
        if parsed.scheme and parsed.netloc:
            return DataSources.URL
        
        # Step 3: Check for typical file path characteristics
        if os.path.isabs(data_source) or "\\" in data_source or "/" in data_source:
            return DataSources.FILE_PATH

 
# Sample usage:
if __name__ == '__main__':
    print(DataSourceIdentifierService().get(data_source="https://www.youtube.com/watch?v=oIPoA22qMvE"))
    print(DataSourceIdentifierService().get(data_source="/users/local/data.txt"))
    print(DataSourceIdentifierService().get(data_source="C:\\Documents\\file.txt"))
