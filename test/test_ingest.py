import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.config import TEST_RAW_WIND_DATA, TEST_STATION_METADATA

from src.data_ingest import fetch_wind_data
import pandas as pd

def test_fetch_wind_data():
    test_data_path = TEST_RAW_WIND_DATA
    test_meta_path = TEST_STATION_METADATA

    df = fetch_wind_data("2024-01-01", "2024-01-10", save_to=test_data_path, station_meta_path=test_meta_path)

    # Test wind readings
    assert isinstance(df, pd.DataFrame), "Output should be a DataFrame"
    assert not df.empty, "DataFrame should not be empty"
    for col in ["timestamp", "station_id", "station_name", "latitude", "longitude", "value"]:
        assert col in df.columns, f"Missing column: {col}"
    assert df["value"].notnull().all(), "Some wind values are missing"
    assert pd.api.types.is_numeric_dtype(df["value"]), "Wind value is not numeric"

    # Test station metadata file
    assert os.path.exists(test_meta_path), "Station metadata CSV was not saved"
    meta_df = pd.read_csv(test_meta_path)
    assert {"station_id", "station_name", "latitude", "longitude"}.issubset(meta_df.columns), "Missing metadata columns"

    print("✅ test_fetch_wind_data passed")

if __name__ == "__main__":
    test_fetch_wind_data()
