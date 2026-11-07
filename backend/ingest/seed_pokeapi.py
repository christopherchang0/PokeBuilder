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
response = requests.get(POKEAPI_URL, timeout=10)
#check if pulled correctly
response.raise_for_status()
data = response.json()
species = {
    "id": data["id"],
    "name": data["name"],
    "generation": int(data["generation"]["url"].rstrip("/").split("/")[-1])
}
print(species)

pokemon_response = requests.get("https://pokeapi.co/api/v2/pokemon/1", timeout=10)
pokemon_response.raise_for_status()
pokemon_data = pokemon_response.json()
stats = {s["stat"]["name"]: s["base_stat"] for s in pokemon_data["stats"]}
pokemon = {
    "id": pokemon_data["id"],
    "species_id": int(pokemon_data["species"]["url"].rstrip("/").split("/")[-1]),
    "name": pokemon_data["name"],
    "is_default": pokemon_data["is_default"],
    "type_1": pokemon_data["types"][0]["type"]["name"],
    "type_2": pokemon_data["types"][1]["type"]["name"] if len(pokemon_data["types"]) > 1 else None,
    "hp": stats["hp"],
    "attack": stats["attack"],
    "defense": stats["defense"],
    "sp_attack": stats["special-attack"],
    "sp_defense": stats["special-defense"],
    "speed": stats["speed"],
}
print(pokemon)

