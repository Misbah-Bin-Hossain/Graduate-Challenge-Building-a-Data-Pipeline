import requests
import json
import urllib3
import pandas as pd
from sqlalchemy import create_engine

# Disable SSL warnings (since we're dealing with an expired certificate)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Base URL for the Star Wars API
base_url = "https://swapi.dev/api/"

print("👥 Getting ALL Star Wars Characters Information...\n")

# Get the first page to see total count
first_response = requests.get(f"{base_url}people/", verify=False)
first_data = first_response.json()
total_people = first_data['count']
print(f"Total people available: {total_people}")

print("\n" + "="*60)

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
        print(f"Retrieved page {page} with {len(data['results'])} characters")
        page += 1
    
    return all_people

# Get all people
print("Fetching all characters from all pages...")
all_characters = get_all_people()
print(f"Successfully retrieved {len(all_characters)} characters!")

print("\n" + "="*60)

"""
# Show all people
print("\n📋 ALL Characters:")
for i, person in enumerate(all_characters, 1):
    print(f"\n{i}. {person['name']}")
    print(f"   Height: {person['height']}cm")
    print(f"   Mass: {person['mass']}kg")
    print(f"   Birth Year: {person['birth_year']}")
    print(f"   Gender: {person['gender']}")

"""
print("\n" + "="*60)
print(f"✅ Done! Retrieved ALL {len(all_characters)} characters from the Star Wars API.")



def insert_people_to_db():
    """
    Insert the already-fetched `all_characters` into PostgreSQL using pandas.to_sql.

    - Reuses the global `all_characters` variable (no re-fetching)
    - Uses pandas/SQLAlchemy (no cursors)
    - Creates table `people` automatically if it doesn't exist
    """

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

    print(f"✅ All done! Inserted {len(df)} rows into 'people' using pandas.to_sql")

# Insert into DB at the end of the script
insert_people_to_db()
