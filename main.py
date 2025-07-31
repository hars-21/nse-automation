from zipfile import ZipFile, BadZipFile
import requests
import pandas as pd
import psycopg2
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import numpy as np
import os
from config import DB_CONN, NSE_REPORTS_URL, MAX_RETRIES, HEADERS


def file_link(url):
    download_link = ""
    for attempt in range(MAX_RETRIES):
        try:
            driver = webdriver.Chrome()
            driver.get(url)
            time.sleep(5)
            divs = driver.find_elements(By.CLASS_NAME, 'reportsDownload')
            for div in divs:
                if "BhavCopy_NSE_CM" in div.text:
                    download_link = div.get_attribute("data-link")
                    break
            driver.quit()

            if not download_link:
                raise Exception("Download link not found on the page.")

            return download_link

        except Exception as e:
            print(f"[ERROR] Attempt {attempt + 1} failed: {e}")
            time.sleep(1)

    print("[FATAL] Failed to fetch download link after retries.")
    return None


def fetch_file(url):
    try:
        res = requests.get(url, headers=HEADERS, stream=True, timeout=10)
        res.raise_for_status()  # Raise error for bad status codes
    except requests.RequestException as e:
        print(f"[ERROR] Failed to download file: {e}")
        return None

    filename = url.split('/')[-1]
    try:
        with open(filename, 'wb') as fd:
            for chunk in res.iter_content(chunk_size=1024):
                fd.write(chunk)
        print(f"[INFO] File downloaded as {filename}")
    except Exception as e:
        print(f"[ERROR] Failed to save file: {e}")
        return None

    try:
        with ZipFile(filename) as data_zip:
            data_zip.extractall()
    except BadZipFile:
        print("[ERROR] Invalid ZIP file.")
        return None
    except Exception as e:
        print(f"[ERROR] Failed to extract ZIP: {e}")
        return None

    extracted_file = filename.split('.')[0]
    print(f"[INFO] File Extracted as {extracted_file}.csv")
    return extracted_file


def clear_files(filename):
    csv_file = f"./{filename}.csv"
    zip_file = f"./{filename}.csv.zip"

    try:
        if os.path.exists(csv_file):
            os.remove(csv_file)
            print(f"[INFO] File '{csv_file}' deleted.")
        else:
            print(f"[WARN] File '{csv_file}' not found.")

        if os.path.exists(zip_file):
            os.remove(zip_file)
            print(f"[INFO] File '{zip_file}' deleted.")
        else:
            print(f"[WARN] File '{zip_file}' not found.")
    except Exception as e:
        print(f"[ERROR] Failed to delete files: {e}")


def store_data(filename):
    try:
        conn = psycopg2.connect(DB_CONN)
        print("[SUCCESS] Connected to DB")
    except Exception as e:
        print(f"[ERROR] Could not connect to database: {e}")
        return 0

    try:
        df = pd.read_csv(f"{filename}.csv")
        df = df.replace({np.nan: None})
        df = df.map(lambda x: x.item() if hasattr(x, 'item') else x)
    except Exception as e:
        print(f"[ERROR] Failed to process CSV file: {e}")
        return 0

    try:
        cur = conn.cursor()
        print("[INFO] Updating DB...")
        for row in df.itertuples(index=False, name=None):
            placeholders = ', '.join(['%s'] * len(row))
            cur.execute(f"INSERT INTO report VALUES ({placeholders})", row)
        conn.commit()
        cur.close()
        conn.close()

        print("[SUCCESS] Database updated successfully!")
        clear_files(filename)
        return 1

    except Exception as e:
        print(f"[ERROR] Failed to insert data into database: {e}")
        conn.rollback()
        conn.close()
        return 0


if __name__ == '__main__':
    site = NSE_REPORTS_URL
    link = file_link(site)

    if not link:
        print("[ABORTED] No file link could be retrieved.")
        exit(1)

    file = fetch_file(link)
    if not file:
        print("[ABORTED] File download or extraction failed.")
        exit(1)

    status = store_data(file)
    if status != 1:
        print("[ABORTED] Data storing failed.")
        exit(1)
