from src.main import LogoDetectionPipeline
import json
from flask import Flask
from flask import jsonify, request
import logging

# Setup app
app = Flask(__name__)

# Setup logger
logging.basicConfig(level=logging.DEBUG)


@app.route('/api/v1/frames/extract/logo', methods=['POST'])
def run_pipeline():
    # Step 1: Load request data
    request_data = json.loads(request.data.decode('utf-8'))
    logging.info(f'{request_data}')
    
    # Step 2: Get service and response
    service = LogoDetectionPipeline()
    response = service.get(**request_data)

    # Step 3: Return response
    return jsonify(response)

# Start server at port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
