import os
import shortuuid
from src.data_handlers.video_util_services import VideoFrameExtractionService, VideoTrimmingService

shortuuid.set_alphabet('1234567890')


def get_short_uuid(length):
    return str(shortuuid.random(length=length))


RUNTIME_DIR = 'data/inference/{iteration_dir}'
PROCESSED_VIDEO_PATH = '{runtime_dir}/cropped.mp4'
FRAMES_DUMP_PATH = '{runtime_dir}/extracted_frames'
    
class FrameTimeStampAssociationService(object):
    def __init__(self):
        super().__init__()
    
    def get(self, **kwargs):
        # Step 1: Declarations
        frame_data = []        
        fps = kwargs.get('fps')
        duration = kwargs.get('duration')
        runtime_dir = kwargs.get('runtime_dir')
        frames_path = FRAMES_DUMP_PATH.format(runtime_dir=runtime_dir)
        
        # Step 2: Calculate the time interval between frames
        interval = 1 / fps
        
        # Step 3: List all frames in the directory, assuming they are named in a sequential order
        frames = sorted(os.listdir(frames_path))
        
        # Step 4: Generate data for each frame
        for i, frame in enumerate(frames):
            # Calculate timestamp for each frame
            timestamp = (i + 1 ) * interval
            if timestamp > duration:
                break  # If the timestamp exceeds the duration, stop adding frames
            frame_data.append({'input_frame': os.path.join(frames_path, frame), 'timestamp': timestamp})
        
        # Step 5: Return the frames data
        return frame_data

class VideoOperationService(object):
    def __init__(self):
        super().__init__()
        self.video_trimming_service = VideoTrimmingService()
        self.frame_extraction_service = VideoFrameExtractionService()
        self.frame_timestamp_association_service = FrameTimeStampAssociationService()
    
    @staticmethod
    def get_kwargs_for_video_trimming_service(**kwargs):
        duration = kwargs.get('duration')
        video_path = kwargs.get('video_path')
        runtime_dir = kwargs.get('runtime_dir')
        kwargs_for_video_trimming_service = dict()
        
        kwargs_for_video_trimming_service['duration'] = duration
        kwargs_for_video_trimming_service['input_video'] = video_path
        kwargs_for_video_trimming_service['output_video'] = PROCESSED_VIDEO_PATH.format(runtime_dir=runtime_dir)
        
        return kwargs_for_video_trimming_service
    
    @staticmethod
    def get_kwargs_for_frame_extraction_service(**kwargs):
        fps = kwargs.get('fps', 10) or 10
        runtime_dir = kwargs.get('runtime_dir')
        kwargs_for_frame_extraction_service = dict()
        
        kwargs_for_frame_extraction_service['fps'] = fps
        kwargs_for_frame_extraction_service['video_path'] = PROCESSED_VIDEO_PATH.format(runtime_dir=runtime_dir)
        kwargs_for_frame_extraction_service['output_dir'] = FRAMES_DUMP_PATH.format(runtime_dir=runtime_dir)
        
        return kwargs_for_frame_extraction_service
        
    def get(self, **kwargs):
        # Step 1: Declarations
        iteration_dir = get_short_uuid(4)
        runtime_dir = RUNTIME_DIR.format(iteration_dir=iteration_dir)
        os.makedirs(runtime_dir, exist_ok=True)
        kwargs['runtime_dir'] = runtime_dir
        
        # Step 2: Perform video trimming
        kwargs_for_video_trimming_service = self.get_kwargs_for_video_trimming_service(**kwargs)
        self.video_trimming_service.get(**kwargs_for_video_trimming_service)
        
        # Step 3: Perform video frame extraction
        get_kwargs_for_frame_extraction_service = self.get_kwargs_for_frame_extraction_service(**kwargs)
        self.frame_extraction_service.get(**get_kwargs_for_frame_extraction_service)
        
        # Step 4: Frames data
        frames_data = self.frame_timestamp_association_service.get(**kwargs)
        
        return frames_data
