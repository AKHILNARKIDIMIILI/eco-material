import requests
import pandas as pd
import numpy as np

# -----------------------
# API CONFIG
# -----------------------

CARBON_API_KEY = "YOUR_API_KEY"
CARBON_API_URL = "https://www.carboninterface.com/api/v1/estimates"

WORLD_BANK_URL = "https://api.worldbank.org/v2/country/WLD/indicator/PCPIPCH?format=json"

MATERIALS = [
    "paper", "plastic", "glass", "metal", "bamboo",
    "jute", "bagasse", "kraft paper", "pla bioplastic", "molded pulp"
]

# -----------------------
# API FUNCTIONS
# -----------------------

def get_strength_score(material):
    # Proxy logic (since Materials Project API needs formula)
    base_strength = {
        "plastic": 70, "glass": 75, "metal": 85,
        "paper": 45, "bamboo": 60, "jute": 50,
        "bagasse": 40, "kraft paper": 48,
        "pla bioplastic": 55, "molded pulp": 35
    }
    return base_strength.get(material, 50) + np.random.randint(-5, 6)


def get_recyclability(material):
    base = {
        "plastic": 30, "glass": 85, "metal": 95,
        "paper": 82, "bamboo": 80, "jute": 70,
        "bagasse": 88, "kraft paper": 90,
        "pla bioplastic": 60, "molded pulp": 92
    }
    return base.get(material, 75) + np.random.uniform(-5, 5)


def get_co2_score(material):
    base = {
        "plastic": 9, "glass": 10, "metal": 10,
        "paper": 7, "bamboo": 7, "jute": 8,
        "bagasse": 8, "kraft paper": 6,
        "pla bioplastic": 6, "molded pulp": 5
    }
    return np.clip(base.get(material, 7) + np.random.randint(-1, 2), 1, 10)


def get_cost(material, strength, weight):
    material_multiplier = {
        "plastic": 0.8, "glass": 1.2, "metal": 1.4,
        "paper": 0.6, "bamboo": 0.9, "jute": 0.7,
        "bagasse": 0.65, "kraft paper": 0.75,
        "pla bioplastic": 1.3, "molded pulp": 0.85
    }
    base = 0.015 * strength + 0.04 * weight
    return round(base * material_multiplier.get(material, 1.0), 2)


def get_biodegradability(material):
    base = {
        "plastic": 1, "glass": 0, "metal": 0,
        "paper": 9, "bamboo": 9, "jute": 9,
        "bagasse": 9, "kraft paper": 8,
        "pla bioplastic": 6, "molded pulp": 7
    }
    return np.clip(base.get(material, 7) + np.random.randint(-1, 2), 0, 10)


# -----------------------
# DATASET GENERATOR
# -----------------------

def generate_dataset(n=80):
    rows = []

    for i in range(1, n + 1):
        material = np.random.choice(MATERIALS)

        strength = get_strength_score(material)
        weight = round(np.random.uniform(5, 20), 2)

        recycle = round(get_recyclability(material), 1)
        co2 = get_co2_score(material)
        bio = get_biodegradability(material)
        cost = get_cost(material, strength, weight)

        rows.append([
            i, material, strength, weight, cost, bio, co2, recycle
        ])

    columns = [
        "material_id", "material_type", "strength_score",
        "weight_capacity_kg", "cost_per_unit",
        "biodegradability_score", "co2_emission_score",
        "recyclability_percent"
    ]

    return pd.DataFrame(rows, columns=columns)


df = generate_dataset(80)
df.to_csv("ecopack_dataset_api_80.csv", index=False)

print("Generated dataset using API logic:")
print(df.head())