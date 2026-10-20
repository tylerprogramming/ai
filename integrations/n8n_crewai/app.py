import hmac
import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from deep_fried.src.deep_fried.main import kickoff

load_dotenv()  # OPENAI_API_KEY and N8N_SHARED_SECRET from .env

app = Flask(__name__)
# No CORS: n8n calls this server-to-server, not from a browser.

# Shared secret that n8n sends in the X-API-Key header (set it in .env)
N8N_SHARED_SECRET = os.getenv("N8N_SHARED_SECRET", "")


@app.before_request
def require_api_key():
    provided = request.headers.get("X-API-Key", "")
    # compare_digest avoids leaking the secret through response timing
    if not N8N_SHARED_SECRET or not hmac.compare_digest(provided.encode(), N8N_SHARED_SECRET.encode()):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401


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
    if not N8N_SHARED_SECRET:
        raise SystemExit("Set N8N_SHARED_SECRET in .env (n8n sends it in the X-API-Key header).")
    host = os.getenv("HOST", "127.0.0.1")
    debug = os.getenv("FLASK_DEBUG") == "1"  # debug is opt-in: FLASK_DEBUG=1
    if debug and host not in ("127.0.0.1", "localhost"):
        # The Werkzeug debugger runs before the API-key check, so never expose it beyond this machine
        raise SystemExit("FLASK_DEBUG=1 is only allowed with HOST=127.0.0.1")
    app.run(
        debug=debug,
        port=int(os.getenv("PORT", "5003")),
        # Local only by default. If n8n runs in Docker, set HOST=0.0.0.0 so the container can reach it.
        host=host,
    )
