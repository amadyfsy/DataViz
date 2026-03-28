from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW = BASE_DIR / "data" / "hospital_data.csv"
DATA_FILE = DATA_RAW  # alias attendu par les notebooks
DATA_PROCESSED = BASE_DIR / "data" / "processed"
VISUALS_DIR = BASE_DIR / "visuals"
RANDOM_STATE = 42
TEST_SIZE = 0.2