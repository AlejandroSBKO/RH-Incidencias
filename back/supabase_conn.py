from supabase import create_client
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv(dotenv_path="config/.env")

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)