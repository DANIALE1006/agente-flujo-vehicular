# Evidencia de Validación de 6 Preguntas Reales (Paso 10 SPED)

Validación del agente con **Groq (`openai/gpt-oss-20b`)** y **Supabase**.

## Pregunta 1: Ranking Flujo Total

**Consulta:** `¿Cuáles fueron los 5 peajes con mayor flujo vehicular total en 2015?`  
**Tiempo de respuesta:** 2.24 s  
**Herramientas ejecutadas:** `[{"herramienta": "ranking_peajes", "parametros": {"anio": 2015, "cantidad": 5, "indicador": "veh_total"}}]`

### Respuesta generada por el agente:

**Resultados del flujo vehicular total (indicador: `veh_total`) – Año 2015**

| Posición | Peaje | Departamento | Flujo total (vehículos) |
|----------|-------|--------------|------------------------|
| 1 | **Chilca** | Lima | 3 060 315 |
| 2 | **El Paraíso** | Lima | 3 024 072 |
| 3 | **Variante de Pasamayo** | Lima | 2 920 572 |
| 4 | **Uchumayo‑Concesión** | Arequipa | 2 740 573 |
| 5 | **Piura Sullana** | Piura | 2 513 422 |

**Interpretación**

- Los tres peajes de Lima dominan el ranking, lo que refleja la alta actividad vial de la capital y sus corredores interurbanos en 2015.
- El peaje “Uchumayo‑Concesión” (Arequipa) y “Piura Sullana” (Piura) están a una distancia considerable de los peajes limeños, lo que sugiere que la movilidad interregional también es sustancial en el periodo analizado.
- Los valores presentados corresponden a datos **observados** completos para el año calendario 2015. No se trata de una estimación o extrapolación; provienen directamente de la tabla `flujo_vehicular` en Supabase.

**Hipótesis preliminar**

- La preponderancia de peajes limeños puede estar relacionada con el incremento del transporte de mercancías y de viajes de pasajeros en la zona metropolitana, posiblemente influido por la expansión de la red de carreteras y la demanda interna durante ese año.

**Nota metodológica**

- Se utilizó el indicador `veh_total` para contar todos los tipos de vehículos.  
- Se respetó la regla de no atribuir causalidad; la asociación observada requiere análisis de causas subyacentes (por ejemplo, cambios en políticas de peaje, obras viales, eventos económicos) para confirmar cualquier relación causal.

---

## Pregunta 2: Ranking Vehículos Pesados

**Consulta:** `¿Cuáles fueron los 3 peajes con mayor tráfico de vehículos pesados en 2015?`  
**Tiempo de respuesta:** 1.51 s  
**Herramientas ejecutadas:** `[{"herramienta": "ranking_peajes", "parametros": {"anio": 2015, "indicador": "veh_pesados_total"}}]`

### Respuesta generada por el agente:

**Indicador utilizado:** veh_pesados_total (tráfico total de vehículos pesados).  
**Periodo analizado:** año 2015 (periodo completo).

| Posición | Peaje | Departamento | Vehículos pesados (total) |
|----------|-------|--------------|---------------------------|
| 1 | Serpentín de Pasamayo | Lima | **2 063 461** |
| 2 | El Paraíso | Lima | **1 706 563** |
| 3 | Uchumayo‑Concesión | Arequipa | **1 449 664** |

Los datos provienen de la tabla `flujo_vehicular` en Supabase y han sido extraídos mediante la función **ranking_peajes**. Los tres peajes con mayor tráfico de vehículos pesados en 2015 son los listados arriba.

---

## Pregunta 3: Comparación Bivariada Departamentos

**Consulta:** `¿Cómo se compara el flujo vehicular total entre Lima e Ica en 2015?`  
**Tiempo de respuesta:** 1.51 s  
**Herramientas ejecutadas:** `[{"herramienta": "comparar_departamentos", "parametros": {"anio": 2015, "departamentos": ["Lima", "Ica"], "indicador": "veh_total"}}]`

### Respuesta generada por el agente:

**Comparación del flujo vehicular total en 2015**

| Departamento | Flujos vehiculares totales (veh_total) |
|--------------|----------------------------------------|
| Lima         | 15 289 151 |
| Ica          | 4 812 165 |

**Interpretación**  
En 2015, Lima registró un flujo vehicular total **3,18 veces mayor** que Ica. Este dato se basa en la tabla `flujo_vehicular` de Supabase y corresponde al indicador *veh_total* para el año 2015.

**Hipótesis**  
La diferencia puede deberse a factores como la mayor densidad poblacional de Lima, su rol como centro económico y la mayor cantidad de rutas de peaje dentro del departamento. Sin embargo, el dato solo muestra una asociación; no se puede afirmar causalidad sin un análisis adicional que incluya variables como la infraestructura vial, la actividad económica y los patrones de viaje.

---

## Pregunta 4: Comparación Multidepartamental

**Consulta:** `¿Qué departamento tuvo mayor flujo vehicular entre Arequipa, Cusco y Puno en 2014?`  
**Tiempo de respuesta:** 1.47 s  
**Herramientas ejecutadas:** `[{"herramienta": "comparar_departamentos", "parametros": {"anio": 2014, "departamentos": ["Arequipa", "Cusco", "Puno"], "indicador": "veh_total"}}]`

### Respuesta generada por el agente:

**Resultado (Indicador: flujo vehicular total – *veh_total*)**  
**Periodo:** Año completo 2014  
**Comparación entre departamentos**: Arequipa, Cusco y Puno

| Departamento | flujo vehicular total (veh_total) |
|---------------|-----------------------------------|
| **Arequipa**  | **5 937 819** vehículos |
| Puno          | 4 069 144 vehículos |
| Cusco         | 1 487 981 vehículos |

**Conclusión**  
En 2014, el departamento con mayor flujo vehicular entre los tres analizados fue **Arequipa**, con un total de 5 937 819 vehículos registrados. Puno ocupó la segunda posición y Cusco la tercera.  

*Fuente de datos:* tabla `flujo_vehicular` en Supabase, función `comparar_departamentos` utilizada con indicador `veh_total`.

---

## Pregunta 5: Ranking Vehículos Ligeros

**Consulta:** `¿Cuál fue el peaje con mayor cantidad de vehículos ligeros en 2015?`  
**Tiempo de respuesta:** 1.49 s  
**Herramientas ejecutadas:** `[{"herramienta": "ranking_peajes", "parametros": {"anio": 2015, "cantidad": 1, "indicador": "veh_ligeros_total"}}]`

### Respuesta generada por el agente:

**Resultado (2015)**  
- **Peaje con mayor cantidad de vehículos ligeros:** **Variante de Pasamayo** (Lima)  
- **Cantidad de vehículos ligeros:** **2 717 109**  

**Interpretación:**  
En el año 2015, el peaje “Variante de Pasamayo” registró el mayor flujo de vehículos ligeros entre todos los peajes analizados. Este dato se obtuvo directamente de la tabla `flujo_vehicular` de Supabase mediante la función de ranking de peajes solicitada.  

**Notas:**  
- El indicador utilizado es `veh_ligeros_total`, que representa el total de vehículos ligeros que transitaron el peaje en el periodo completo del año.  
- No se inferirá causalidad; el valor simplemente refleja la observación más alta en el conjunto de datos.

---

## Pregunta 6: Análisis Contextual de Periodos

**Consulta:** `¿Cuáles fueron los 5 principales peajes por flujo en 2026 y qué advertencia temporal aplica?`  
**Tiempo de respuesta:** 3.69 s  
**Herramientas ejecutadas:** `[{"herramienta": "ranking_peajes", "parametros": {"anio": 2026, "cantidad": 5, "indicador": "veh_total"}}]`

### Respuesta generada por el agente:

**Top 5 peajes por flujo total en 2026**

| Posición | Peaje | Departamento | Flujos (vehículos totales) |
|----------|-------|--------------|---------------------------|
| 1 | Chilca | Lima | 3 006 618 |
| 2 | Jahuay Chincha | Ica | 1 463 812 |
| 3 | Variante de Pasamayo | Lima | 1 459 359 |
| 4 | Chicama | La Libertad | 1 269 478 |
| 5 | Ica | Ica | 1 236 694 |

**Advertencia temporal**

- **Período de 2026**: La tabla *flujo_vehicular* solo contiene datos de enero‑octubre de 2026 (hasta la fecha de la última actualización).  
- **Implicación**: Los valores de flujo son **observados** y no deben extrapolarse directamente a un año completo sin ajustar por la parte faltante. Cualquier comparación con años completos (por ejemplo, 2025, 2024, etc.) debe considerar que 2026 corresponde a un periodo parcial, lo que puede provocar subestimaciones en los totales anuales.

---

*Datos utilizados*: Ranking del indicador `veh_total` para el año 2026. No se inferirá causalidad, solo se presentan las cifras observadas.

---

