import os
from dotenv import load_dotenv
import psycopg
import requests

load_dotenv()

SUPABASE_DATABASE_URL = os.getenv("SUPABASE_DATABASE_URL")
conn = psycopg.connect(SUPABASE_DATABASE_URL)
# 2. Open a cursor to perform database operations
with conn.cursor() as cur:
    # 3. Execute the query
    cur.execute("SELECT 1;")

    # 4. Fetch the result
    result = cur.fetchone()
    print(result)  # Outputs: (1,)

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon-species/1"
species = {}
response = requests.get(POKEAPI_URL, timeout=10)
#check if pulled correctly
response.raise_for_status()
data = response.json()
species["id"] = data["id"]
species["name"] = data["name"]
species["generation"] = data["generation"]["url"].rstrip("/").split("/")[-1]
print(species)

