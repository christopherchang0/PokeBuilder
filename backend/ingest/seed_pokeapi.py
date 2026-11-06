import os
from dotenv import load_dotenv
import psycopg

load_dotenv()

SUPABASE_DATABASE_URL = os.getenv("SUPABASE_DATABASE_URL")