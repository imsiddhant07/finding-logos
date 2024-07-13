import os

from src.data_handlers.frames_dumping_service import AnnotatedFramesDumpingService
from src.utils.video_util_services import VideoCreationService


class BoxedVideoGenerationService(object):
    """Service to generated annotated video."""
    def __init__(self):
        super().__init__()
        self.video_creation_service = VideoCreationService()
        self.frames_dumping_service = AnnotatedFramesDumpingService()
        
    def get(self, **kwargs):
        kwargs_for_video_creation_service = dict()
        
        parent_dir = self.frames_dumping_service.get(**kwargs)

        kwargs_for_video_creation_service = kwargs.copy()
        kwargs_for_video_creation_service['frames_dir'] = os.path.join(parent_dir, 'result_frames')
        kwargs_for_video_creation_service['output_video_path'] = os.path.join(parent_dir, 'output.mp4')
        self.video_creation_service.get(**kwargs_for_video_creation_service)
