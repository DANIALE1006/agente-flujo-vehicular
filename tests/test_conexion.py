import sys
import os

# Agrega la carpeta principal del proyecto a la ruta de búsqueda de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


from servicios.supabase_client import supabase
from config import TABLE_NAME

def test_conexion():
    print("\n--- PROBANDO PASO 2: CONEXIÓN PYTHON - SUPABASE ---")
    r = supabase.table(TABLE_NAME).select("*").limit(5).execute()
    
    assert r.data is not None, "Error: No se obtuvieron datos de Supabase"
    print(f"✅ Conexión exitosa. Se recuperaron {len(r.data)} registros:")
    
    for fila in r.data:
        # Busca la clave en mayúsculas o minúsculas según la estructura de Supabase
        peaje = fila.get('NOMBRE_PEAJE') or fila.get('nombre_peaje')
        depto = fila.get('DEPARTAMENTO') or fila.get('departamento')
        print(f" - Peaje: {peaje}, Departamento: {depto}")

if __name__ == "__main__":
    test_conexion()