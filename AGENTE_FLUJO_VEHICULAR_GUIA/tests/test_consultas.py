import sys
import os

# Agrega la carpeta principal del proyecto a la ruta de búsqueda de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from herramientas.consultas import ranking_peajes
from herramientas.analisis import construir_ranking_peajes

def test_ranking_2015():
    print("\n--- PROBANDO PASO 4: RANKING DE PEAJES (2015) ---")
    datos = ranking_peajes(2015, "veh_total", 5)
    ranking = construir_ranking_peajes(datos, "veh_total", 5)
    
    print("\nRanking de Peajes 2015:")
    for i, r in enumerate(ranking, 1):
        print(f" {i}. {r['nombre_peaje']} ({r['departamento']}): {r['veh_total']} vehículos")
    
    assert len(ranking) > 0, "El ranking no debe estar vacío"
    assert len(ranking) <= 5, "No debe exceder la cantidad solicitada de 5 registros"
    print("\n✅ PASO 4 (2015) COMPLETADO EXITOSAMENTE")

def test_ranking_2025_fallback():
    print("\n--- PROBANDO PASO 4: RANKING DE PEAJES CON FALLBACK (2025) ---")
    datos = ranking_peajes(2025, "veh_total", 5)
    ranking = construir_ranking_peajes(datos, "veh_total", 5)
    
    print("\nRanking de Peajes (Fallback 2025):")
    for i, r in enumerate(ranking, 1):
        print(f" {i}. {r['nombre_peaje']} ({r['departamento']}): {r['veh_total']} vehículos")
        
    assert len(ranking) <= 5, "No debe exceder la cantidad solicitada de 5 registros"
    print("\n✅ PASO 4 (FALLBACK) COMPLETADO EXITOSAMENTE")

if __name__ == "__main__":
    test_ranking_2015()
    test_ranking_2025_fallback()