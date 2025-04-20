from flask import Flask, request, jsonify
from flask_cors import CORS
from deep_fried.src.deep_fried.main import kickoff
from datetime import datetime

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

@app.route('/process', methods=['POST'])
def process_request():
    # Get the JSON data from the request
    data = request.get_json()
    print(data)
    
    result = kickoff(data)

    # This is just a sample response
    sample_response = {
        "status": "success",
        "message": "Request processed successfully",
        "received_data": data,
        "sample_result": {
            "task": "completed",
            "timestamp": datetime.now().strftime("%Y-%m-%d"),
            "response": result
        }
    }
    
    return jsonify(sample_response)

if __name__ == '__main__':
    app.run(debug=True, port=5003, host='0.0.0.0') 