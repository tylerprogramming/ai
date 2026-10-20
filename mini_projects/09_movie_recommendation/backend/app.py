import os

from flask import Flask, request, jsonify
from flask_cors import CORS

from movieflow.src.movieflow.main import kickoff

app = Flask(__name__)

# Configure CORS properly
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173"],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    movies = kickoff(request_files=request.files, request_form=request.form)
    
    if movies is None:
        return jsonify({"error": "No valid input provided"}), 400
    
    return jsonify({"movies": movies})

if __name__ == '__main__':
    # debug is opt-in (FLASK_DEBUG=1); localhost only, the Vite frontend calls http://localhost:5555
    app.run(debug=os.getenv('FLASK_DEBUG') == '1', host='127.0.0.1', port=5555) 