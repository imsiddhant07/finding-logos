"""
File will get the frame-timestamp data
Perform inference for all frames and send back response
"""
import os
import logging
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from src.inference_handlers.yolo_inference_service import YOLOInferenceService
from src.utils.batching_service import BatchingService

# Setup logger
logging.basicConfig(level=logging.DEBUG)

EXTRACTION_SERVICE_MAPPING = {
    'yolo': YOLOInferenceService()
}


class FramesInfoExtractionService(object):
    """A service class for extracting information from frames using relevant extraction process."""
    def __init__(self):
        super().__init__()
        self.batching_service = BatchingService()
    
    def get(self, **kwargs):
        """Extracts information from frames_data using the specified extraction_method.

        Args:
        - frames_data (List[Dict[str, Any]]): List of dictionaries containing frame data.
                Each dictionary should at least contain 'input_frame' key.
        - extraction_method (str): Method used for extracting information from frames.

        Returns:
        - List[Dict[str, Any]]: Updated frames_data with 'result' key added for each frame.

        """
        # Step 1: Declarations
        results = list()
        input_frames = list()
        kwargs_for_batching_service = dict()
        
        frames_data = kwargs.get('frames_data')
        extraction_method = kwargs.get('extraction_method')
        
        
        num_workers = os.cpu_count() or multiprocessing.cpu_count()  # Decide number of workers for multiprocessing based on available cores.
        extraction_service = EXTRACTION_SERVICE_MAPPING.get(extraction_method)
        
        logging.info(f'Num workers : {num_workers} | Extraction method : {extraction_method}')
        
        # Step 2: Iterate over frame data to create data object for extraction method
        for data in frames_data:
            input_frame = data.get('input_frame')
            input_frames.append(input_frame)
        
        kwargs_for_batching_service['records_list'] = input_frames
        batches = self.batching_service.get(**kwargs_for_batching_service)

        for batch in batches:
            result = extraction_service.get(image_paths=batch)
            results.extend(result)
        
        # Step 3: Ececute the extraction service (Multiprocessing for optimisation)
        # with ProcessPoolExecutor(max_workers=num_workers) as executor:
        #     results = list(executor.map(extraction_service.get(), data_for_extraction_service))

        # Step 4: Update the frames data with results
        for idx, result in enumerate(results):
            frames_data[idx]['result'] = result
        
        # Step 5: Return the frames_data
        return frames_data
        
        