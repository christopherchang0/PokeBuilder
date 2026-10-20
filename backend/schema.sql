CREATE TABLE pokemon_species (
  id INT PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE,
  generation INT NOT NULL
);

CREATE TABLE pokemon (
  id INT PRIMARY KEY,
  species_id INT NOT NULL REFERENCES pokemon_species(id),
  name VARCHAR(50) NOT NULL UNIQUE,
  is_default BOOLEAN NOT NULL,
  type_1 VARCHAR(50) NOT NULL,
  type_2 VARCHAR(50),
  hp INT NOT NULL,
  attack INT NOT NULL,
  defense INT NOT NULL,
  sp_attack INT NOT NULL,
  sp_defense INT NOT NULL,
  speed INT NOT NULL
)