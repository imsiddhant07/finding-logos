## Pipeline to detect logos


### Problem statement
Given a video return a json file with labels associated with each timestamp frame.

------------
### Input:
Video in mp4 format. | 
[Video via link or local path](https://www.youtube.com/watch?v=oIPoA22qMvE)

### Output:

```json
{
    "label_1": [10.1, 10.2, 10.5, 21.3, ..],
    "label_2": [9.4, 10.2, ..]
}
```

Updated the response format:
```
{
    "cocacola": [
        {
            "timestamp": 1.0,
            "xywh": [56, 45, 12, 13]
        }
    ],
    "pepsi": [
        {
            "timestamp": 2.0,
            "xywh": [51, 43, 12, 13]
        },
        {
            "timestamp": 3.0,
            "xywh": [51, 43, 12, 13]
        }
    ]
}
```

</br>

------------


### Steps involved:

1. Get video from source (link/local path).
2. Move video/image frame to relevant data directory.
```
video_path : String

|-- DataRetrieverService : Makes sure data is present is relevant directory.

    |-- DataSourceIdentifierService : Identifies the scope of data (local_path or url)

    |-- Based on identifies data source perform either of:
        |-- DataDownloadService : Downloads data to directory.
        |-- DataMovementService : Moves data to directory.
```
3. Extract frames from video.
```
saved_path : String
duration : Integer
fps : Integer

|-- VideoOperationService : Does necessary operations on video data.

    |-- VideoTrimmingService : Trimes the video to given duration.
    |-- VideoFrameExtractionService : Extracts frames based on given trimmed video.
    |-- FrameTimeStampAssociationService : Create a data object for frames and timestamp association.    

```
4. Run necessary pre-processing on frames prior to inference.
5. Run inference
```

|-- FramesInfoExtractionService : Does necessary operations on video data.
    |-- YOLOInferenceService : Inference service to get logo data.
```
5. Build the response as per labels.
```
ResponseBuilderService
|-- ResponseBuilderService : Does necessary operations on video response.
``` 
5. Dump to a json file.
```
|-- JSONDumpingService: Dumps the data into a json file specified at request.
```
6. Create a annotated video ( - Experimental Quality might be at the lower end here)
```
|-- BoxedVideoGenerationService: The service dumps the result frames and generates a video based on it.
    |-- VideoCreationService: Service generates video based on frames.
    |-- AnnotatedFramesDumpingService: Dumps frames to directory. 
```

<br>

-----------
<br>

Usage:
(make sure you have docker and docker-compose installed and setup in your system)

```bash
cd finding-logos

docker-compose up --build  # This will start the server at port: 4000.
```

Sample curl:
```bash
curl --location 'http://localhost:4000/api/v1/frames/extract/logo' \
--header 'Content-Type: application/json' \
--data '{
    "duration": 30,
    "fps": 2,
    "extraction_method": "yolo",
    "video_path": "https://www.youtube.com/watch?v=oIPoA22qMvE",
    "json_path": "data/inference/response.json"
}'
```