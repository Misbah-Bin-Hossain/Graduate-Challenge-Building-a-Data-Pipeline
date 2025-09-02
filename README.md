# Star Wars Data Pipeline

This project fetches data from the Star Wars API (SWAPI) and stores it in a PostgreSQL database using Python and pandas.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.7 or higher
- Install packages from `requirements.txt`

## Database Setup (Docker Compose)

Run the following in Windows PowerShell from the project directory.

Start the database
```powershell
docker-compose up -d
```

Check that the container is running
```powershell
docker ps
```

Database connection details

- Host: localhost
- Port: 5432
- Database: starwars_db
- Username: starwars_misbah
- Password: misbah

Stop the database when finished
```powershell
docker-compose down
```

Remove the database and its data (use with care)
```powershell
docker-compose down -v
```

## How to Run the Pipeline

Install Python dependencies
```powershell
pip install -r requirements.txt
```

Run the script that fetches and inserts data
```powershell
python ".\Get Data.py"
```

## What the Script Does

1. Calls function `get_all_people` to fetch all people from SWAPI.
2. Saves the results in variable `all_characters`.
3. Calls function `insert_people_to_db` to write the data into PostgreSQL using pandas `to_sql` into a table named `people`.

## Functions Used

- `get_all_people`: requests data from SWAPI across all pages.
- `insert_people_to_db`: converts data into a pandas DataFrame and inserts into PostgreSQL using SQLAlchemy engine and pandas `to_sql`.

## Libraries Used

- `requests`: HTTP requests to the API
- `urllib3`: disables SSL warning for this API call
- `pandas`: tabular data handling and `to_sql` insertion
- `sqlalchemy`: database engine creation for pandas
- `psycopg2` (used via SQLAlchemy): PostgreSQL driver

## Verify Data

Method 1: simple check script
```powershell
python ".\check data.py"
```

Method 2: psql inside the container
```powershell
docker exec -it starwars_postgres psql -U starwars_misbah -d starwars_db
```
Then run inside psql
```
\dt
SELECT COUNT(*) FROM people;
SELECT * FROM people LIMIT 10;
```

## Automate Daily Run (Windows Task Scheduler)

Create a small PowerShell script to run the pipeline and schedule it daily with Task Scheduler.

1) Create `run_pipeline.ps1` in the project directory
```powershell
Set-Location "C:\Github\The challenge\Graduate-Challenge-Building-a-Data-Pipeline"
docker-compose up -d
python ".\Get Data.py" *>> ".\pipeline.log"
```

2) Create a scheduled task
- Open Task Scheduler → Create Task…
- General: Name = StarWarsPipelineDaily; Run whether user is logged on or not
- Triggers: New → Daily → set time
- Actions: New → Start a program
  - Program/script: powershell.exe
  - Add arguments: `-ExecutionPolicy Bypass -File "C:\Github\The challenge\Graduate-Challenge-Building-a-Data-Pipeline\run_pipeline.ps1"`
  - Start in: `C:\Github\The challenge\Graduate-Challenge-Building-a-Data-Pipeline`
- Settings: Enable "Run task as soon as possible after a scheduled start is missed"

3) Test the task
- Right-click the task → Run
- Check `pipeline.log` for output and errors

Notes
- Ensure Python and required packages are installed on the machine (use `pip install -r requirements.txt`).
- If you prefer a fixed Python, use its full path in the script (for example, `C:\Users\<you>\AppData\Local\Microsoft\WindowsApps\python3.11.exe`).
- If you see encoding errors in logs, remove emojis from prints (already done) or run Python with UTF-8: `python -X utf8 ".\Get Data.py"`.

## Project Structure

```
├── docker-compose.yml          # PostgreSQL container configuration
├── Get Data.py                 # Fetches SWAPI people and inserts into Postgres
├── check data.py               # Preview of inserted data using pandas and SQLAlchemy
├── requirements.txt            # Python dependencies
└── README.md                   # This guide
```

## Troubleshooting

- If port 5432 is busy, change `docker-compose.yml` ports from "5432:5432" to "5433:5432" and connect to `localhost:5433` in the scripts.
- If the container does not start, ensure Docker is running and check logs with
```powershell
docker-compose logs postgres
```
- If modules are missing, reinstall requirements
```powershell
pip install -r requirements.txt
```

## Quick Reference

Start DB
```powershell
docker-compose up -d
```

Install packages
```powershell
pip install -r requirements.txt
```

Run pipeline
```powershell
python ".\Get Data.py"
```

Check data
```powershell
python ".\check data.py"
```