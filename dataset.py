import pandas as pd
import json

def get_dataset():
    """Load dataset from shl_catalog.json and return it as a pandas DataFrame."""
    with open("shl_catalog.json", "r") as f:
        data = json.load(f)
    return pd.DataFrame(data)
