import os
import datetime
import requests
import smulogin
import time
from fetcher import fetch_week_event
from aggregate import aggregate
from export import export_to_ics
import ddddocr
from io import BytesIO
from PIL import Image

# Monkey patch get_captcha to allow custom solver
def solve_captcha(session, captcha_response):
    img = Image.open(BytesIO(captcha_response.content))
    ocr = ddddocr.DdddOcr(beta=True)
    result = ocr.classification(img)
    return result

def headless_get_captcha(session):
    headers_captcha = {
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    }
    captcha_response = session.get(smulogin.captcha_url, headers=headers_captcha)
    return solve_captcha(session, captcha_response)

# Apply patch
smulogin.get_captcha = headless_get_captcha

# Monkey patch login to raise exception on failure
original_login = smulogin.login
def strict_login(account, password, session):
    max_retries = 5
    for attempt in range(max_retries):
        print(f"Login attempt {attempt + 1}/{max_retries}...")
        captcha = smulogin.get_captcha(session)
        ticket = smulogin.sendlogin(account, password, captcha, session)
        if ticket:
            smulogin.redirect_login(session, ticket)
            return
        print("Login failed (likely CAPTCHA error), retrying...")
        time.sleep(1)
    
    raise Exception(f"Login failed after {max_retries} attempts")

smulogin.login = strict_login

def main():
    # Read config from env
    account = os.environ.get("SMU_ACCOUNT")
    password = os.environ.get("SMU_PASSWORD")
    weeks_str = os.environ.get("SEMESTER_WEEKS", "20")
    start_date_str = os.environ.get("START_DATE")
    if not all([account, password, start_date_str]):
        print("Error: Missing environment variables. Please set SMU_ACCOUNT, SMU_PASSWORD, and START_DATE.")
        exit(1)

    weeks = int(weeks_str)
    
    try:
        y, m, d = map(int, start_date_str.split('-'))
        start_date = datetime.date(y, m, d)
    except ValueError:
        print("Error: Invalid START_DATE format. Use YYYY-M-D.")
        exit(1)

    session = requests.Session()
    
    print("Logging in...")
    try:
        smulogin.login(account, password, session)
    except Exception as e:
        print(f"Login failed: {e}")
        exit(1)

    print("Fetching events...")
    se = list(fetch_week_event(session, 1, weeks))
    
    if not se:
        print("No events found or fetch failed.")
        exit(1)

    print(f"Found {len(se)} events. Exporting to ICS...")
    ics_content = export_to_ics(se, start_date)
    
    with open("schedule.ics", "w", encoding="utf-8") as f:
        f.write(ics_content)
    
    print("Successfully exported to schedule.ics")

if __name__ == "__main__":
    main()
