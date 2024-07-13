from src.main import LogoDetectionPipeline
import json
from flask import Flask
from flask import jsonify, request
import logging

app = Flask(__name__)

# Setup logger
logging.basicConfig(level=logging.DEBUG)


@app.route('/api/v1/frames/extract/logo', methods=['POST'])
def run_pipeline():
    request_data = json.loads(request.data.decode('utf-8'))
    logging.debug(f"Accessing the home page {request_data}")
    logging.info(f'{request_data}')
    service = LogoDetectionPipeline()

    response = service.get(**request_data)

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
