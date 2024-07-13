import logging

from src.data_handlers.input_data_handler_service import DataRetrieverService
from src.data_handlers.video_operation_service import VideoOperationService
from src.inference_handlers.video_frames_info_extraction_service import FramesInfoExtractionService
from src.results_services.response_builder_service import ResponseBuilderService
from src.utils.json_dumping_service import JSONDumpingService

# Setup logger
logging.basicConfig(level=logging.DEBUG)


class LogoDetectionPipeline(object):
    def __init__(self):
        super().__init__()
        self.video_retriever_service = DataRetrieverService()
        self.video_operation_service = VideoOperationService()
        self.frame_info_extraction_service = FramesInfoExtractionService()
        self.response_builder_service = ResponseBuilderService()
        self.response_dumping_service = JSONDumpingService()

    def get(self, **kwargs):
        kwargs_for_response_dumping_service = dict()
        kwargs_for_response_builder_service = dict()
        kwargs_for_video_retriever_service = dict()
        kwargs_for_video_operation_service = dict()
        kwargs_for_info_extraction_service = dict()
        
        extraction_method = kwargs.get('extraction_method')
        video_path = kwargs.get('video_path')
        json_path = kwargs.get('json_path')
        duration = kwargs.get('duration')
        fps = kwargs.get('fps')

        # Step 1: Get data to destination directory
        kwargs_for_video_retriever_service['data_source'] = video_path
        saved_path = self.video_retriever_service.get(
            **kwargs_for_video_retriever_service)
        
        # Step 2: Build `kwargs_for_video_operation` and get frames data
        kwargs_for_video_operation_service['video_path'] = saved_path
        kwargs_for_video_operation_service['duration'] = duration
        kwargs_for_video_operation_service['fps'] = fps
        frames_data = self.video_operation_service.get(**kwargs_for_video_operation_service)
        
        # Step 3: Build `kwargs_for_info_extraction` and get frame wise results
        kwargs_for_info_extraction_service['extraction_method'] = extraction_method
        kwargs_for_info_extraction_service['frames_data'] = frames_data
        results = self.frame_info_extraction_service.get(**kwargs_for_info_extraction_service)
        
        # Step 4: Build `kwargs_for_response_builder` and get response
        kwargs_for_response_builder_service['results'] = results
        response = self.response_builder_service.get(**kwargs_for_response_builder_service)
        
        # Step 5: Build `kwargs_for_response_dumping` and get response
        kwargs_for_response_dumping_service['json_path'] = json_path
        kwargs_for_response_dumping_service['json_object'] = response
        self.response_dumping_service.get(**kwargs_for_response_dumping_service)

        # logging.info(f'Saved video to {saved_path} | Created frames at {frames_data} | results {results}')
        logging.info(f'Saved video to {saved_path} | Created frames at {frames_data}')
        
        return response
