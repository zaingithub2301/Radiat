import pandas as pd

# --------------------------
# Bronze Layer - Raw Data Ingestion
# --------------------------

# Function to load data based on file type (CSV)
def load_utility_data(file_path):
    return pd.read_csv(file_path)

# Ingest and process raw data files for each utility
def bronze_layer_ingestion(utility_paths):
    raw_data = {}
    for utility, paths in utility_paths.items():
        # Loading network, installed DER, and planned DER data for each utility
        raw_data[utility] = {
            "network_data": load_utility_data(paths["network"]),
            "installed_der": load_utility_data(paths["installed"]),
            "planned_der": load_utility_data(paths["planned"]),
        }
    return raw_data

# Paths for example CSV files
utility_paths = {
    "utility1": {
        "network": "data/utility1_network.csv",
        "installed": "data/utility1_installed.csv",
        "planned": "data/utility1_planned.csv"
    },
    "utility2": {
        "network": "data/utility2_network.csv",
        "installed": "data/utility2_installed.csv",
        "planned": "data/utility2_planned.csv"
    }
}

# Ingest data
bronze_data = bronze_layer_ingestion(utility_paths)
print("Bronze Layer Data Ingested:\n", bronze_data)


# --------------------------
# Silver Layer - Standardization and Cleaning
# --------------------------

# Function to standardize and clean network data
def standardize_network_data(df, utility_name):
    # Standardize column names and apply transformations if needed
    df = df.rename(columns={
        "feeder_segment_id": "feeder_id",  # Example renaming
        "hosting_capacity": "max_hosting_capacity"
    })
    df["utility_name"] = utility_name
    return df

# Standardize and concatenate data across all utilities
def silver_layer_standardization(bronze_data):
    standardized_data = {
        "network_data": pd.DataFrame(),
        "installed_der": pd.DataFrame(),
        "planned_der": pd.DataFrame()
    }

    for utility, datasets in bronze_data.items():
        # Standardize each dataset type
        standardized_data["network_data"] = pd.concat([
            standardized_data["network_data"],
            standardize_network_data(datasets["network_data"], utility)
        ])
        # Add utility name for installed and planned DER data
        standardized_data["installed_der"] = pd.concat([
            standardized_data["installed_der"],
            datasets["installed_der"].assign(utility_name=utility)
        ])
        standardized_data["planned_der"] = pd.concat([
            standardized_data["planned_der"],
            datasets["planned_der"].assign(utility_name=utility)
        ])

    return standardized_data

# Standardize data
silver_data = silver_layer_standardization(bronze_data)
print("\nSilver Layer Standardized Data:\n", silver_data)


# --------------------------
# Platinum Layer - API-Ready Tables
# --------------------------

# Create API-ready tables for high-performance querying
def create_platinum_tables(silver_data):
    # Filter feeders based on a minimum hosting capacity requirement
    feeders_with_capacity = silver_data["network_data"][silver_data["network_data"]["max_hosting_capacity"] > 0]

    # Combine installed and planned DER data for unified querying by feeder_id
    installed_and_planned_der = pd.concat([
        silver_data["installed_der"],
        silver_data["planned_der"]
    ])

    return {
        "feeders_with_capacity": feeders_with_capacity,
        "installed_and_planned_der": installed_and_planned_der
    }

# Create Platinum tables
platinum_data = create_platinum_tables(silver_data)
print("\nPlatinum Layer API-Ready Tables:\n", platinum_data)


# --------------------------
# Query Functions for API
# --------------------------

# Query feeders with a hosting capacity above a given threshold
def query_feeders_with_capacity(capacity_threshold, platinum_data):
    return platinum_data["feeders_with_capacity"][platinum_data["feeders_with_capacity"]["max_hosting_capacity"] > capacity_threshold]

# Query installed and planned DER records by feeder ID
def query_der_by_feeder(feeder_id, platinum_data):
    return platinum_data["installed_and_planned_der"][platinum_data["installed_and_planned_der"]["feeder_id"] == feeder_id]


# Example queries for testing
if __name__ == "__main__":
    capacity_threshold = 100  # Example threshold
    feeder_id = "feeder123"   # Example feeder ID

    # Retrieve feeders with capacity above threshold
    feeders_above_threshold = query_feeders_with_capacity(capacity_threshold, platinum_data)
    print("\nFeeders with capacity above threshold:\n", feeders_above_threshold)

    # Retrieve installed and planned DER for specific feeder
    der_for_feeder = query_der_by_feeder(feeder_id, platinum_data)
    print("\nInstalled and planned DER for feeder:\n", der_for_feeder)
