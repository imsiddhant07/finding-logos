import os
import logging
import subprocess

# Setup logger
logging.basicConfig(level=logging.DEBUG)


class VideoFrameExtractionService(object):
    """A service class for extracting frames from a video using ffmpeg."""
    def __init__(self):
        super().__init__()
        
    def get(self, **kwargs):
        """Extracts frames from the video located at video_path and saves them in output_dir.

        Args:
        - video_path (str): Path to the input video file.
        - output_dir (str): Directory where extracted frames will be saved.
        - fps (float, optional): Frames per second to extract. Defaults to 10.

        Raises:
            subprocess.CalledProcessError: If ffmpeg command execution fails.
        """
        # Step 1: Declarations
        output_dir = kwargs.get('output_dir')
        video_path = kwargs.get('video_path')
        fps = kwargs.get('fps', 10) or 10
        
        # Step 2: Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Step 3: Construct ffmpeg command to extract frames
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', video_path,            # Input video path
            '-vf', f'fps={fps}',         # Frames per second to extract
            f'{output_dir}/frame_%06d.jpg'  # Output file pattern
        ]
        
        # Step 4: Execute ffmpeg command
        subprocess.run(ffmpeg_cmd, check=True)


class VideoTrimmingService(object):
    """A service class for trimming video segments using ffmpeg."""
    def __init__(self):
        super().__init__()
    
    def get(self, **kwargs):
        """Trims the input_video to the specified duration and saves it as output_video.

        Args:
        - input_video (str): Path to the input video file.
        - output_video (str): Path where trimmed video will be saved.
        - duration (float, optional): Duration of the trimmed video segment in seconds. Defaults to 10.
        """
        logging.info(f'kwargs from trimmer {kwargs}')
        # Step 1: Declarations
        input_video = kwargs.get('input_video')
        output_video = kwargs.get('output_video')
        duration = kwargs.get('duration', 10) or 10  # Note: Incase the duration is longer than length of video, it will by default return the video as is.
        
        # os.makedirs(output_video, exist_ok=True)
                     
        # Step 2: Construct the ffmpeg command as a list of arguments
        ffmpeg_command = [
            'ffmpeg',            # The ffmpeg command
            '-i', input_video,   # Input video file
            '-t', str(duration), # Duration of cropped segment in seconds
            '-c:v', 'copy',      # Video codec copy
            '-c:a', 'copy',      # Audio codec copy
            output_video         # Output video file
        ]
        
        # Step 3: Execute the ffmpeg command
        subprocess.run(ffmpeg_command)
        
        
class VideoCreationService(object):
    """A service class for create video from frames using ffmpeg."""
    def __init__(self):
        super().__init__()
    
    def get(self, **kwargs):
        """
        Create a video from frames using ffmpeg.

        Args:
            frames_dir (str): Directory containing the frames.
            output_video_path (str): Path to save the output video.
            fps (int, optional): Frames per second for the output video. Defaults to 25.

        Returns:
            None
        """
        output_video_path = kwargs.get('output_video_path')
        frames_dir = kwargs.get('frames_dir')
        fps = kwargs.get('fps')
        
        # Step 1: Check if the frames directory exists
        if not os.path.exists(frames_dir):
            raise FileNotFoundError(f"Frames directory '{frames_dir}' does not exist.")
        
        # Step 2: Construct ffmpeg command to create video from frames
        ffmpeg_cmd = [
            'ffmpeg',
            '-framerate', str(fps),       # Frames per second of the output video
            '-pattern_type', 'glob',      # Use glob pattern for image input
            '-i', f'{frames_dir}/*.jpg',  # Input frames pattern (assuming JPG format)
            '-c:v', 'libx264',            # Output video codec
            '-pix_fmt', 'yuv420p',        # Pixel format
            output_video_path             # Output video file path
        ]
        
        # Step 3: Execute ffmpeg command
        subprocess.run(ffmpeg_cmd)