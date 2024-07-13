from src.constants.infernce_constants import LogoLabels


class ResponseBuilderService(object):
    def __init__(self):
        super().__init__()
    
    def get(self, **kwargs):
        # Step 1: Declarations
        results = kwargs.get('results')
        
        response = dict()
        label_0_list = list()
        label_1_list = list()
        
        # Step 2: Iterate over results
        for frame_result in results:
            timestamp = frame_result.get('timestamp')
            result = frame_result.get('result')
            boxes = result.boxes

            # Step 2b: Get prediction results 
            prediction_classes = boxes.cls.cpu().detach().tolist()
            boxes_coordinates = boxes.xywh.cpu().detach().tolist()
            
            for idx, pred_class in enumerate(prediction_classes):
                obj = dict()
                obj['timestamp'] = timestamp
                obj['xywh'] = boxes_coordinates[idx]
                
                if pred_class == 0:
                    label_0_list.append(obj)
                
                else:
                    label_1_list.append(obj)
                    
        # Step 3: Build response            
        response[LogoLabels.COCACOLA] = label_0_list
        response[LogoLabels.PEPSI] = label_1_list
        
        return response