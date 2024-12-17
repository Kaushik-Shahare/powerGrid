import random
from datetime import datetime

# Define regions in Vadodara with mock coordinates (latitude and longitude)
regions = [
    {"name": "Alkapuri", "latitude": 22.3121, "longitude": 73.1810},
    {"name": "Gotri", "latitude": 22.3080, "longitude": 73.1624},
    {"name": "Manjalpur", "latitude": 22.2730, "longitude": 73.1903},
    {"name": "Waghodia", "latitude": 22.3107, "longitude": 73.2194},
    {"name": "Fatehgunj", "latitude": 22.3181, "longitude": 73.1855},
]

# Define possible energy sources
energy_sources = ["Solar", "Wind", "Thermal", "Hydro"]

# Function to generate random weather conditions
def generate_weather():
    conditions = ["Sunny", "Cloudy", "Rainy", "Windy"]
    return {
        "condition": random.choice(conditions),
        "temperature": round(random.uniform(20, 40), 1),  # Temperature in Celsius
        "humidity": random.randint(30, 90),  # Humidity percentage
    }

# Function to generate energy production data
def generate_energy_data():
    region = random.choice(regions)
    source = random.choice(energy_sources)
    energy_produced = round(random.uniform(50, 500), 2)  # Energy produced in kWh
    weather = generate_weather()
    
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "region": {
            "name": region["name"],
            "latitude": region["latitude"],
            "longitude": region["longitude"]
        },
        "energy_source": source,
        "energy_produced_kwh": energy_produced,
        "weather": weather
    }
