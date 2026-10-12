# PokeBuilder

Want a Pokemon on your team but don't know what the other 5 should be? We've got you covered.

Right now, Pokemon players spend hours working out which Pokemon best complement one they really like. PokeBuilder solves exactly that problem.

> 💡 Instead of spending hours manually figuring out the best possible team for a given Pokemon, we do that for you. Give us a Pokemon you want on your team, and we will automatically build a team around its capabilities. Using AI, we give personalized recommendations and feedback on your team at many levels. Whether you're playing through the game or battling competitively, there's something for everyone!

## User Workflow

1. User creates a profile or logs in
2. User selects a Pokemon to add
3. Ask if the user wants to customize that Pokemon (Shadcn Command menu)
4. Ask if the user wants to follow a certain Gen or Format. If yes:
   1. Allow the user to choose moves, EVs, and/or items
   2. Checkboxes for whether the Pokemon should serve certain functions (e.g. Gigantamax, Z-Moves)
5. User sends the information to the backend, which passes it to the AI components to build a personalized team
6. Team is created based on the Pokemon and selected options
7. New team is presented to the user. The user can write suggestions, which go back to the AI
8. Export the team to PokePaste, then import it into Pokemon Showdown

## Tech Stack

**Frontend**
- Node.js
- Shadcn UI
- Tailwind CSS

**Backend**
- Python
  - PyTorch (safetensors)
  - Pandas
  - Scikit-learn (joblib)
  - NumPy
- FastAPI
- PostgreSQL

**Data**
- Supabase
- Cloudflare

**Platform**
- AWS
- Docker

**APIs / Datasets**
- Data: [Smogon Stats Archive](https://www.smogon.com/stats/)
- APIs: [PokeAPI](https://pokeapi.co/), [Pokemon Showdown](https://pokemonshowdown.com/)

## Architecture

### Phase 1: Ingestion & Database Seeding

1. Write a local Python script using `requests` to pull static Pokemon data from **PokeAPI** (types, base stats, movesets) and batch-insert it into the **Supabase PostgreSQL** database.
2. Download historical battle data files from the **Smogon Stats Archive**. Use **Pandas** to parse the text summaries or JSON into clean arrays of teams.

### Phase 2: Training the Engine

1. Vectorize the cleaned team dataset using **NumPy**.
2. Build the machine learning model. Start with a fast K-Nearest Neighbors (KNN) model using **Scikit-learn** to match complementary teammates by cosine similarity, then experiment with a custom **PyTorch** network.
3. Save the trained models locally using `joblib` or `safetensors`.

### Phase 3: Creating the Communication Bridge

1. Build the **FastAPI** server. On startup, it loads the `.safetensors` or `.joblib` model into memory. A POST route `/api/v1/recommend` takes an input Pokemon and runs it through the loaded model.
2. Spin up the **Node.js** frontend. Set up a backend route or Server Action that uses `fetch()` to send requests to the FastAPI server.

### Phase 4: Polish & Deployment

1. Build the data-dense frontend layout using **Tailwind CSS** and **Shadcn UI** components (e.g. Command menus for search, Dialog modals for team analysis).
2. Write a `Dockerfile` for the frontend and one for the backend. Test them together locally with Docker Compose before pushing the containers to **AWS**.

## Project Structure

```
PokeBuilder/
├── backend/   # FastAPI server, ML models, ingestion scripts
├── data/      # Smogon / PokeAPI datasets
└── frontend/  # Node.js + Shadcn UI + Tailwind app
```
