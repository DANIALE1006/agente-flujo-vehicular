import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from herramientas.consultas import datos_departamentos
from herramientas.analisis import composicion_vehicular, comparar_departamentos

def test_composicion():
    print("\n--- PROBANDO COMPOSICIÓN VEHICULAR ---")
    datos = [
        {"veh_ligeros_total": 60, "veh_pesados_total": 40},
        {"veh_ligeros_total": 40, "veh_pesados_total": 60},
    ]
    r = composicion_vehicular(datos)
    assert r["veh_total_calculado"] == 200
    assert r["pct_ligeros"] == 50.0
    print("✅ Prueba de composición aprobada")

def test_comparacion_departamentos_2015():
    print("\n--- PROBANDO PASO 5: COMPARACIÓN DE DEPARTAMENTOS (2015) ---")
    deptos = ["LIMA", "ICA"]
    
    datos = datos_departamentos(2015, deptos, "veh_total")
    resultado = comparar_departamentos(datos, "veh_total")
    
    print("\nResultado de Comparación de Departamentos (2015):")
    for r in resultado:
        print(f" - {r['departamento']}: {r['veh_total']} vehículos")
    
    assert len(resultado) > 0, "La comparación no debe estar vacía"
    print("\n✅ PASO 5 (2015) COMPLETADO EXITOSAMENTE")

def test_comparacion_departamentos_fallback():
    print("\n--- PROBANDO PASO 5: COMPARACIÓN DE DEPARTAMENTOS (FALLBACK 2025) ---")
    deptos = ["LIMA", "ICA"]
    
    datos = datos_departamentos(2025, deptos, "veh_total")
    resultado = comparar_departamentos(datos, "veh_total")
    
    print("\nResultado de Comparación de Departamentos (Fallback):")
    for r in resultado:
        print(f" - {r['departamento']}: {r['veh_total']} vehículos")
        
    assert len(resultado) > 0, "La comparación no debe estar vacía"
    print("\n✅ PASO 5 (FALLBACK) COMPLETADO EXITOSAMENTE")

if __name__ == "__main__":
    test_composicion()
    test_comparacion_departamentos_2015()
    test_comparacion_departamentos_fallback()