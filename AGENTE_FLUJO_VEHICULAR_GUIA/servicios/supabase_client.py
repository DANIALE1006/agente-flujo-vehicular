"""Cliente único de Supabase para el proyecto."""
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Configure SUPABASE_URL y SUPABASE_KEY en .env")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
