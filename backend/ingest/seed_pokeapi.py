import os
from dotenv import load_dotenv
import psycopg

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