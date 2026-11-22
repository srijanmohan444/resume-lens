import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "data" / "app.db"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite").strip()
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "").strip()
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "").strip()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "").strip()
JSEARCH_HOST = os.getenv("JSEARCH_HOST", "jsearch.p.rapidapi.com").strip()
CACHE_TTL_HOURS = float(os.getenv("CACHE_TTL_HOURS", "12"))

MAX_UPLOAD_BYTES = 5 * 1024 * 1024

CITIES = [
    "All India", "Remote", "Bengaluru", "Hyderabad", "Pune", "Mumbai", "Delhi NCR",
    "Gurugram", "Noida", "Chennai", "Kolkata", "Ahmedabad", "Jaipur",
    "Chandigarh", "Kochi", "Indore",
]
# Adzuna's India site uses some older city names.
ADZUNA_WHERE = {"Bengaluru": "Bangalore", "Delhi NCR": "Delhi"}