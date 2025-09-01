import requests
import json
import urllib3

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
print("🔄 Fetching all characters from all pages...")
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
    print(f"   Hair Color: {person['hair_color']}")
    print(f"   Skin Color: {person['skin_color']}")
    print(f"   Eye Color: {person['eye_color']}")
    print(f"   Birth Year: {person['birth_year']}")
    print(f"   Gender: {person['gender']}")

"""

print("\n" + "="*60)
print(f"✅ Done! Retrieved ALL {len(all_characters)} characters from the Star Wars API.")

