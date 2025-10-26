import os
import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from .chatbot import CHATBOT

# Load environment variables from .env file
load_dotenv()

# Configure logging for the Flask app
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/api/v1/query', methods=['POST'])
def query_chatbot():
    """
    API endpoint for querying the customer support chatbot.
    Expects a JSON body with a 'query' field.
    """
    if CHATBOT is None:
        logger.error("Chatbot service is unavailable.")
        return jsonify({"error": "Chatbot service is unavailable."}), 503

    data = request.get_json()
    if not data or 'query' not in data:
        logger.warning("Received request with missing 'query' field.")
        return jsonify({"error": "Missing 'query' field in request body."}), 400

    user_query = data.get('query')
    logger.info(f"Received query: {user_query}")
    
    response_text = CHATBOT.get_response(user_query)

    return jsonify({
        "query": user_query,
        "response": response_text,
        "source": "NovaPay Customer Support Chatbot (LightRAG)"
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    status = "ok" if CHATBOT is not None else "degraded"
    logger.info(f"Health check status: {status}")
    return jsonify({
        "status": status,
        "service": "NovaPay Chatbot API"
    })

if __name__ == '__main__':
    # Get port from environment variables, default to 5000
    port = int(os.getenv('FLASK_PORT', 5000))
    # Running on 0.0.0.0 to be accessible from outside the container/environment
    app.run(host='0.0.0.0', port=port)
