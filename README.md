# 📊 NSE BhavCopy Downloader & PostgreSQL Uploader

This project automates the extraction of the **BhavCopy_NSE_CM** report from [NSE India](https://www.nseindia.com/all-reports), processes the CSV inside the ZIP, stores the data in a PostgreSQL database, and cleans up local files — all with solid error handling.


## ✅ Features

- 🔁 Retry logic to handle transient scraping issues
- 🌐 Automated link scraping with Selenium
- 📥 Secure ZIP download & extraction
- 📊 CSV cleaning with pandas & NumPy
- 🗃️ PostgreSQL database storage
- 🧹 Local file cleanup
- 🧯 Robust exception handling

---

## 🧱 Tech Stack

- Python 3.12
- Selenium
- Requests
- pandas + NumPy
- psycopg2
- PostgreSQL
- ChromeDriver

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/nse-bhavcopy-downloader.git
cd nse-bhavcopy-downloader
```


### 2. Install Dependencies

```bash
pip install selenium requests pandas numpy psycopg2-binary
```

> ✅ Make sure Chrome and [ChromeDriver](https://sites.google.com/chromium.org/driver/) are installed and accessible in your PATH.



### 3. Configure Your Environment

#### Create `.env` file (do **not** push this to GitHub):

```env
DB_NAME=your_db_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 4. Prepare Your PostgreSQL Database

Create a table matching the CSV structure. For example:

```sql
CREATE TABLE IF NOT EXISTS report(
TradDt DATE,
BizDt DATE,
Sgmt VARCHAR(20),
Src VARCHAR(20),
FinInstrmTp VARCHAR(20),
FinInstrmId INT,
ISIN VARCHAR(20),
TckrSymb VARCHAR(20),
SctySrs VARCHAR(20),
XpryDt DATE,
FininstrmActlXpryDt DATE,
StrkPric FLOAT,
OptnTp VARCHAR(20),
FinInstrmNm VARCHAR(50),
OpnPric FLOAT,
HghPric FLOAT,
LwPric FLOAT,
ClsPric FLOAT,
LastPric FLOAT,
PrvsClsgPric FLOAT,
UndrlygPric FLOAT,
SttlmPric FLOAT,
OpnIntrst VARCHAR(20),
ChngInOpnIntrst VARCHAR(20),
TtlTradgVol INT,
TtlTrfVal FLOAT,
TtlNbOfTxsExctd INT,
SsnId VARCHAR(20),
NewBrdLotQty INT,
Rmks VARCHAR(20),
Rsvd1 VARCHAR(20),
Rsvd2 VARCHAR(20),
Rsvd3 VARCHAR(20),
Rsvd4 VARCHAR(20),
id SERIAL PRIMARY KEY);
```

## 5. Run the Script

```bash
python main.py
```

This will:

1. Scrape the BhavCopy download link from NSE
2. Download and extract the `.csv.zip` file
3. Load and clean the CSV using pandas
4. Insert data into your PostgreSQL table
5. Delete the temporary files afterward



## 🧪 Sample Log Output

```
[INFO] File downloaded as cm30JUL2025bhav.csv.zip
[SUCCESS] Database updated successfully!
[INFO] File 'cm30JUL2025bhav.csv' deleted.
[INFO] File 'cm30JUL2025bhav.csv.zip' deleted.
```


## 📌 Project Structure

```bash
.
├── main.py           # Main script with scraping, DB upload, and cleanup
├── config.py         # Configuration loader (uses .env)
├── .env              # Environment secrets (not pushed to Git)
├── README.md         # Project documentation
```


## 👨‍💻 Author

**Your Name**
GitHub: [@hars-21](https://github.com/hars-21)
