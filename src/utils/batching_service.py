class BatchingService(object):
    def __init__(self):
        super().__init__()
    
    def get(self, **kwargs):
        batch_size = kwargs.get('batch_size', 8) or 8
        records_list = kwargs.get('records_list')
        
        for i in range(0, len(records_list), batch_size):
            yield records_list[i:i + batch_size]
