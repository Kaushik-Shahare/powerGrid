from flask import Flask, jsonify, request

app = Flask(__name__)

# Route to accept JSON data (POST) and return JSON response
@app.route('/api/echo', methods=['POST'])
def echo_json():
    # Get JSON data from the request
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    # Example: Modify or echo back the received JSON
    response = {
        "message": "JSON data received successfully!",
        "received_data": data
    }
    return jsonify(response), 200

# Route to send predefined JSON data (GET)
@app.route('/api/data', methods=['GET'])
def send_json():
    # Example JSON response
    data = {
        "id": 1,
        "name": "Flask Example",
        "description": "This is a sample JSON response",
        "status": "success"
    }
    return jsonify(data), 200

# Default Route
@app.route('/')
def home():
    return "Welcome to the JSON Flask Server!"

# Run the server
if __name__ == '__main__':
    app.run(debug=True, port=5000)
