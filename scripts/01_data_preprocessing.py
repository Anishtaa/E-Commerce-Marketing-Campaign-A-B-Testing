# 01_data_preprocessing.py
import pandas as pd
import os

# ------------------------------
# Paths
# ------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "marketing_campaign.csv")
CLEAN_DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_campaign.csv")

# ------------------------------
# Load dataset
# ------------------------------
def load_data(path):
    """Load the raw dataset with proper delimiter"""
    df = pd.read_csv(path, delimiter=";")  # <- semicolon is key
    print("Data loaded successfully. Shape:", df.shape)
    return df

# ------------------------------
# Clean dataset
# ------------------------------
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean dataset by removing duplicates and handling missing values"""

    # Strip spaces from column names
    df.columns = df.columns.str.strip()

    # Drop duplicates
    df = df.drop_duplicates()

    # Handle missing Income
    if "Income" in df.columns:
        df = df.dropna(subset=["Income"])
    else:
        print("⚠️ 'Income' column not found!")

    # Fill missing categorical columns with 'Unknown'
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].fillna("Unknown")

    return df

# ------------------------------
# Save cleaned dataset
# ------------------------------
def save_data(df, path):
    """Save cleaned dataset with semicolon separator"""
    df.to_csv(path, index=False, sep=";")  # <- keep ; separator
    print("Cleaned data saved to:", path)

# ------------------------------
# Main
# ------------------------------
if __name__ == "__main__":
    df_raw = load_data(RAW_DATA_PATH)
    df_clean = clean_data(df_raw)
    save_data(df_clean, CLEAN_DATA_PATH)
