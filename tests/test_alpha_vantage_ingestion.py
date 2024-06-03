import unittest
from unittest.mock import path, MagicMock
import pandas as pd
from scripts.data_ingestion.alpha_vantage_ingestion import (
    fetch_alpha_vantage_data,
    transform_data_to_dataframe,
    upload_to_s3
)

class TestAlphaVantageIngestion(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()