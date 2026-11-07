import os
from dotenv import load_dotenv
import psycopg
import requests
from pathlib import Path
import json


load_dotenv()


# Cache setup
CACHE_DIR = Path(__file__).resolve().parents[2] / "data" / "pokeapi"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def fetch_json(url):
    # e.g. .../api/v2/pokemon/1 -> pokemon_1.json
    filename = url.rstrip("/").split("/api/v2/")[-1].replace("/", "_") + ".json"
    path = CACHE_DIR / filename

    if path.exists():
        with open(path) as f:
            return json.load(f)

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    temp_path = path.with_suffix(".tmp")

    with open(temp_path, "w") as f:
        json.dump(data, f)
    temp_path.replace(path)
    return data

def id_from_url(url):
    id = int(url["generation"]["url"].rstrip("/").split("/")[-1])
    return id


# POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon-species/1"
# data = fetch_json(POKEAPI_URL)

def parse_species(data):
    species = {
        "id": data["id"],
        "name": data["name"],
        "generation": id_from_url(data["generation"]["url"])
    }
    return species

# pokemon_data = fetch_json("https://pokeapi.co/api/v2/pokemon/1")
def parse_pokemon(pokemon_data):
    stats = {s["stat"]["name"]: s["base_stat"] for s in pokemon_data["stats"]}
    pokemon = {
        "id": pokemon_data["id"],
        "species_id": id_from_url(pokemon_data["species"]["url"]),
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
    return pokemon

def insert_species(cur, species):
    cur.execute("""
    INSERT INTO pokemon_species (id, name, generation)
    VALUES (%(id)s, %(name)s, %(generation)s)
    ON CONFLICT (id) DO UPDATE SET
        name = EXCLUDED.name,
        generation = EXCLUDED.generation
    """,
    species,
    )
def insert_pokemon(cur, pokemon):
    cur.execute(
        """
        INSERT INTO pokemon (id, species_id, name, is_default, type_1, type_2,
                            hp, attack, defense, sp_attack, sp_defense, speed)
        VALUES (%(id)s, %(species_id)s, %(name)s, %(is_default)s, %(type_1)s, %(type_2)s,
                %(hp)s, %(attack)s, %(defense)s, %(sp_attack)s, %(sp_defense)s, %(speed)s)
        ON CONFLICT (id) DO UPDATE SET
            species_id = EXCLUDED.species_id,
            name = EXCLUDED.name,
            is_default = EXCLUDED.is_default,
            type_1 = EXCLUDED.type_1,
            type_2 = EXCLUDED.type_2,
            hp = EXCLUDED.hp,
            attack = EXCLUDED.attack,
            defense = EXCLUDED.defense,
            sp_attack = EXCLUDED.sp_attack,
            sp_defense = EXCLUDED.sp_defense,
            speed = EXCLUDED.speed
        """,
        pokemon,
    )



#steps
#double loop. Outer loop builds species, inner builds the pokemon