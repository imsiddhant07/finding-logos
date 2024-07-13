from enum import Enum


class DataSources(str, Enum):
    URL = 'url'
    FILE_PATH = 'file_path'
