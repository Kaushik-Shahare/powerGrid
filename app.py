from flask import Flask, jsonify, request
import json
import sqlite3
from modules.energy_production import generate_energy_data
from modules.energy_demand import generate_demand_data
from modules.gemini import ai_assistant

# Initialize Flask app
app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('energy_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS energy_production (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            energy_produced_kwh REAL NOT NULL,
            energy_source TEXT NOT NULL,
            region_name TEXT NOT NULL,
            region_latitude REAL NOT NULL,
            region_longitude REAL NOT NULL,
            timestamp TEXT NOT NULL,
            weather_condition TEXT NOT NULL,
            weather_humidity INTEGER NOT NULL,
            weather_temperature REAL NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS energy_demand (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area TEXT NOT NULL,
            is_commercial BOOLEAN NOT NULL,
            num_units INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            total_demand_kwh REAL NOT NULL,
            unit_demands TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Endpoint for energy production data
@app.route('/api/energy-production', methods=['GET'])
def energy_production_api():
    data = generate_energy_data()
    conn = sqlite3.connect('energy_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO energy_production (
            energy_produced_kwh, energy_source, region_name, region_latitude, region_longitude, 
            timestamp, weather_condition, weather_humidity, weather_temperature
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['energy_produced_kwh'], data['energy_source'], data['region']['name'], 
        data['region']['latitude'], data['region']['longitude'], data['timestamp'], 
        data['weather']['condition'], data['weather']['humidity'], data['weather']['temperature']
    ))
    conn.commit()
    conn.close()
    return jsonify(data)

# Helper function to convert rows to dictionary with column names
def row_to_dict(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

# Endpoint to get all energy production data
@app.route('/api/energy-production/all', methods=['GET'])
def get_all_energy_production():
    conn = sqlite3.connect('energy_data.db')
    conn.row_factory = row_to_dict
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM energy_production')
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

# Endpoint to get energy production data by ID
@app.route('/api/energy-production/<int:id>', methods=['GET'])
def get_energy_production_by_id(id):
    conn = sqlite3.connect('energy_data.db')
    conn.row_factory = row_to_dict
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM energy_production WHERE id = ?', (id,))
    row = cursor.fetchone()
    conn.close()
    return jsonify(row)

# Endpoint for energy demand data
@app.route('/api/energy-demand', methods=['GET'])
def energy_demand_api():
    area_name = request.args.get("area_name", "Unknown Area")
    is_commercial = request.args.get("is_commercial", "false").lower() == "true"
    num_units = int(request.args.get("num_units", 100))
    
    data = generate_demand_data(area_name, is_commercial, num_units)
    conn = sqlite3.connect('energy_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO energy_demand (
            area, is_commercial, num_units, timestamp, total_demand_kwh, unit_demands
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data['area'], data['is_commercial'], data['num_units'], data['timestamp'], 
        data['total_demand_kwh'], json.dumps(data['unit_demands'])
    ))
    conn.commit()
    conn.close()
    return jsonify(data)

# Endpoint to get all energy demand data
@app.route('/api/energy-demand/all', methods=['GET'])
def get_all_energy_demand():
    conn = sqlite3.connect('energy_data.db')
    conn.row_factory = row_to_dict
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM energy_demand')
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

# Endpoint to get energy demand data by ID
@app.route('/api/energy-demand/<int:id>', methods=['GET'])
def get_energy_demand_by_id(id):
    conn = sqlite3.connect('energy_data.db')
    conn.row_factory = row_to_dict
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM energy_demand WHERE id = ?', (id,))
    row = cursor.fetchone()
    conn.close()
    return jsonify(row)

@app.route("/api/ai-assistant", methods=["POST"])
def ai_endpoint():
    return ai_assistant()

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5000)
