import requests
import json
import urllib3
import pandas as pd
from sqlalchemy import create_engine

# Disable SSL warnings (since we're dealing with an expired certificate)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Base URL for the Star Wars API
base_url = "https://swapi.dev/api/"

print("Getting Star Wars Characters Data\n\n")

# Get the first page to see total count
first_response = requests.get(f"{base_url}people/", verify=False)
first_data = first_response.json()
total_people = first_data['count']
print(f"Total people available: {total_people} \n")


# Function to get all people from all pages
def get_all_people():
    all_people = []
    page = 1
    
    while True:
        url = f"{base_url}people/?page={page}"
        response = requests.get(url, verify=False)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error on page {page}: Status code {response.status_code}")
            break
            
        data = response.json()

        # Check if we have results and if they're valid
        if 'results' not in data or not data['results']:
            print(f"No more results on page {page}")
            break
            
        all_people.extend(data['results'])
        print(f"Retrieved {len(data['results'])} characters from page{page}")
        page += 1
    
    return all_people

# Get all people
print("Fetching all characters from all pages...")
all_characters = get_all_people()
print(f"Successfully got data of {len(all_characters)} characters from API\n")


# Function to insert data into database
def insert_people_to_db():

    # 1) Convert the list of characters to simple rows
    simple_rows = []
    for person in all_characters:
        simple_rows.append({
            "name": person.get("name"),
            "height": person.get("height"),
            "mass": person.get("mass"),
            "birth_year": person.get("birth_year"),
            "gender": person.get("gender"),
        })

    # 2) Create DataFrame
    df = pd.DataFrame(simple_rows)

    # 3) Create SQLAlchemy engine (credentials from docker-compose.yml)
    engine = create_engine(
        "postgresql+psycopg2://starwars_misbah:misbah@localhost:5432/starwars_db"
    )

    # 4) Append to table 'people'; create if not exists
    df.to_sql("people", engine, if_exists="append", index=False)

    print(f"\nInserted {len(df)} rows into Table: 'people' of DB: starwars_db using pandas\n")

# Insert into DB at the end of the script
insert_people_to_db()
