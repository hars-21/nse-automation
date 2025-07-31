from dotenv import load_dotenv
import os

load_dotenv()

DB_CONN = os.environ["DB_URL"]

NSE_REPORTS_URL = "https://www.nseindia.com/all-reports"
MAX_RETRIES = 2

HEADERS = {
    'User-Agent': 'Mozilla/5.0'
}
