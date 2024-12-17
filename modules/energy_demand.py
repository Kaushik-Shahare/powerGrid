import random
from datetime import datetime

# Define demand profiles for residential and commercial areas
demand_profiles = {
    "residential": {"min": 5, "max": 20},  # Energy demand in kWh per household
    "commercial": {"min": 50, "max": 200}  # Energy demand in kWh per unit
}

# Function to generate energy demand for a given area
def generate_demand_data(area_name, is_commercial=False, num_units=100):
    """
    Simulates energy demand for an area.
    :param area_name: Name of the area being simulated.
    :param is_commercial: Boolean indicating whether the area is commercial.
    :param num_units: Number of households or commercial units in the area.
    :return: A dictionary with demand data.
    """
    profile = demand_profiles["commercial" if is_commercial else "residential"]
    
    # Calculate total energy demand
    demand_per_unit = [
        round(random.uniform(profile["min"], profile["max"]), 2)
        for _ in range(num_units)
    ]
    total_demand = round(sum(demand_per_unit), 2)

    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "area": area_name,
        "is_commercial": is_commercial,
        "num_units": num_units,
        "total_demand_kwh": total_demand,
        "unit_demands": demand_per_unit  # Individual demands for households or units
    }
