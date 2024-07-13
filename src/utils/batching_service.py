class BatchingService(object):
    """A service class for batching records_list into batches of specified size."""
    def __init__(self):
        super().__init__()
    
    def get(self, **kwargs):
        """
        Batches records_list into batches of batch_size.

        Args:
        - records_list (List[Any]): List of records to be batched.
        - batch_size (int, optional): Size of each batch. Defaults to 8.

        Yields:
            Generator[List[Any], None, None]: Yields batches of records_list.

        Notes:
            - Uses Python's generator to yield batches iteratively.
        """
        batch_size = kwargs.get('batch_size', 8) or 8
        records_list = kwargs.get('records_list')
        
        for i in range(0, len(records_list), batch_size):
            yield records_list[i:i + batch_size]
