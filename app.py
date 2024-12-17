from flask import Flask, jsonify, request
from modules.energy_production import generate_energy_data
from modules.energy_demand import generate_demand_data
from modules.gemini import ai_assistant

# Initialize Flask app
app = Flask(__name__)


# Endpoint for energy production data
@app.route('/api/energy-production', methods=['GET'])
def energy_production_api():
    data = generate_energy_data()
    return jsonify(data)


# Endpoint for energy demand data
@app.route('/api/energy-demand', methods=['GET'])
def energy_demand_api():
    area_name = request.args.get("area_name", "Unknown Area")
    is_commercial = request.args.get("is_commercial", "false").lower() == "true"
    num_units = int(request.args.get("num_units", 100))
    
    data = generate_demand_data(area_name, is_commercial, num_units)
    return jsonify(data)


@app.route("/api/ai-assistant", methods=["POST"])
def ai_endpoint():
    return ai_assistant()

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5000)
