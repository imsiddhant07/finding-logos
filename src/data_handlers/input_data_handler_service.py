import os
import shutil
from pytube import YouTube
import logging

from src.data_handlers.constants import DataSources
from src.data_handlers.input_data_indentifier_service import DataSourceIdentifierService

DESTINATION_FOLDER = 'data/inference'
# Setup logger
logging.basicConfig(level=logging.DEBUG)


class DataDownloadService(object):
    """Class to download data from YouTube"""
    def __init__(self):
        super().__init__()
        
    def get(self, **kwargs):
        """
        Args:
        ** kwargs: Arbitary keyword arguments.
        - data_source (str): data source path.

        Returns:
        - saved_path(str): path of data object        
        """
        # Step 1: Declrations 
        data_source = kwargs.get('data_source')
        path = DESTINATION_FOLDER
        
        # Step 2: Get video and save to destination folder
        youtube = YouTube(data_source)
        video = youtube.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        saved_path = video.download(path)
        
        # Step 3: Return saved path
        return saved_path


class DataMovementService(object):
    """Class to move data from source to destination directory"""
    def __init__(self):
        super().__init__()
        
    def get(self, **kwargs):
        """
        Args:
        ** kwargs: Arbitary keyword arguments.
        - data_source (str): data source path.

        Returns:
        - destination_path(str): path of data object
        """
        # Step 1: Declaraions
        data_source = kwargs.get('data_source')
        
        # Step 2a: Extract the filename from the source path
        filename = os.path.basename(data_source)
        # Step 2b: Construct the full destination path
        destination_path = os.path.join(DESTINATION_FOLDER, filename)
        # Step 2c: Move the file
        shutil.copy(data_source, destination_path)
        
        # Step 3: Return the destination path 
        return destination_path


DATASOURCE_SERVICE_MAPPING = {
    DataSources.FILE_PATH: DataMovementService(),
    DataSources.URL: DataDownloadService()
}


class DataRetrieverService(object):
    """Class to return path of data object post Download/movement based on source type."""
    def __init__(self):
        super().__init__()
        self.data_source_identifer_service = DataSourceIdentifierService()

    def get(self, **kwargs):
        """
        Args:
        ** kwargs: Arbitary keyword arguments.
        - data_source (str): data source path.

        Returns:
        - path(str): path of data object
        """
        # Step 1: Declarations
        data_source = kwargs.get('data_source')
        kwargs_for_data_source_indentifer_service = dict()
        kwargs_for_data_service = dict()
        
        # Step 2: Get data source identity
        kwargs_for_data_source_indentifer_service['data_source'] = data_source
        data_source_identity = self.data_source_identifer_service.get(**kwargs_for_data_source_indentifer_service)
        
        # Step 3: Get relevant data service based of source identity
        data_service = DATASOURCE_SERVICE_MAPPING.get(data_source_identity)
        
        # Step 4: Invoke the data service
        kwargs_for_data_service['data_source'] = data_source
        path = data_service.get(**kwargs_for_data_service)
        
        return path