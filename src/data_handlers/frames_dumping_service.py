import os


class AnnotatedFramesDumpingService(object):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def get_parent_directory_before(file_path, keyword):
        """
        Get the parent directory path before a specific keyword in a file path.

        Args:
            file_path (str): Full file path containing the keyword.
            keyword (str): Keyword to find the directory path before.

        Returns:
            str: Parent directory path before the keyword.
        """
        # Find the position of the last occurrence of the keyword
        index = file_path.rfind(keyword)
        
        # If keyword not found, return the original file_path
        if index == -1:
            return file_path
        
        # Get the substring before the keyword
        parent_directory = file_path[:index]
        
        # Clean up path using os.path.dirname to remove any extra slashes
        parent_directory = os.path.dirname(parent_directory)
        
        return parent_directory

    def get(self, **kwargs):
        results = kwargs.get('results')
        
        dummy_object = results[0]
        dummy_frame_path = dummy_object.get('input_frame')
        
        parent_directory = self.get_parent_directory_before(
            file_path=dummy_frame_path, 
            keyword='extracted_frames'
        )
        
        # Create the 'result_frames' directory if it doesn't exist
        os.makedirs(os.path.join(parent_directory, 'result_frames'), exist_ok=True)
        
        for idx, frame_result in enumerate(results):
            result = frame_result.get('result')
            result.save(filename=os.path.join(parent_directory, 'result_frames', f'result_{idx+1}.jpg'))
            
        return parent_directory