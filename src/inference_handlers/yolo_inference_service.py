from ultralytics import YOLO
MODEL_PATH = 'artefacts/models/weights/best.pt'

class YOLOInferenceService(object):
    def __init__(self):
        super().__init__()
        
    def get(self, **kwargs):
        # Step 1: Declarations
        image_paths = kwargs.get('image_paths')
        model = YOLO(MODEL_PATH)
        
        # Step 2: Inference
        results = model(image_paths)
        
        #Step 3: Return results
        return results
        