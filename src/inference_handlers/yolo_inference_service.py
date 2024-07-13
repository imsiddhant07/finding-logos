from ultralytics import YOLO
MODEL_PATH = 'artefacts/models/weights/best.pt'

class YOLOInferenceService(object):
    """A service class for performing YOLO object detection inference on images."""
    def __init__(self):
        super().__init__()
        
    def get(self, **kwargs):
        """Performs YOLO object detection inference on given image_paths.

        Args:
        - image_paths (List[str]): List of file paths to images for inference.

        Returns:
        - List[DetectionResult]: List of detection results for each image.
        """
        # Step 1: Declarations
        image_paths = kwargs.get('image_paths')
        model = YOLO(MODEL_PATH)
        
        # Step 2: Inference
        results = model(image_paths)
        
        #Step 3: Return results
        return results
        