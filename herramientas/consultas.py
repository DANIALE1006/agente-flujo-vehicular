"""Consultas a la base de datos de flujo vehicular en Supabase."""
from config import TABLE_NAME
from servicios.supabase_client import supabase

INDICADORES_PERMITIDOS = [
    "veh_total",
    "veh_imd",
    "veh_ligeros_total",
    "veh_pesados_total",
]

MAPA_INDICADORES = {
    "flujo": "veh_total",
    "flujo_vehicular": "veh_total",
    "flujo_total": "veh_total",
    "total": "veh_total",
    "veh_total": "veh_total",
    "imd": "veh_imd",
    "veh_imd": "veh_imd",
    "ligeros": "veh_ligeros_total",
    "veh_ligeros": "veh_ligeros_total",
    "veh_ligeros_total": "veh_ligeros_total",
    "pesados": "veh_pesados_total",
    "veh_pesados": "veh_pesados_total",
    "veh_pesados_total": "veh_pesados_total",
}

MAPA_DEPARTAMENTOS_TILDES = {
    "ancash": "Áncash",
    "san martin": "San Martín",
    "apurimac": "Apurímac",
    "junin": "Junín",
    "huanuco": "Huánuco",
}


def normalizar_indicador(indicador: str) -> str:
    """Normaliza sinónimos de indicadores a los nombres reconocidos por la base de datos."""
    ind = str(indicador or "").strip().lower()
    return MAPA_INDICADORES.get(ind, ind)


def ranking_peajes(anio: int, indicador: str = "veh_total", cantidad: int = 5) -> list[dict]:
    """
    Obtiene los registros necesarios para construir el ranking de peajes.
    Soporta fallback si el año solicitado no cuenta con registros directos.
    """
    indicador_norm = normalizar_indicador(indicador)
    if indicador_norm not in INDICADORES_PERMITIDOS:
        raise ValueError(
            f"Indicador no permitido: '{indicador}'. Opciones válidas: {INDICADORES_PERMITIDOS}"
        )

    indicador_upper = indicador_norm.upper()

    # 1. Consulta para el año solicitado
    res = (
        supabase.table(TABLE_NAME)
        .select(f"NOMBRE_PEAJE,DEPARTAMENTO,{indicador_upper},ANIO,MES")
        .eq("ANIO", int(anio))
        .execute()
    )
    data = res.data if res and res.data else []

    # 2. Fallback: Si no hay registros para ese año específico, consultar registros disponibles más recientes
    if not data:
        res_fallback = (
            supabase.table(TABLE_NAME)
            .select(f"NOMBRE_PEAJE,DEPARTAMENTO,{indicador_upper},ANIO,MES")
            .order("ANIO", desc=True)
            .limit(1000)
            .execute()
        )
        data = res_fallback.data if res_fallback and res_fallback.data else []

    return data


def datos_departamentos(anio: int, departamentos: list[str], indicador: str = "veh_total") -> list[dict]:
    """Obtiene datos para comparar departamentos soportando variantes de texto y fallback de año."""
    indicador_norm = normalizar_indicador(indicador)
    if indicador_norm not in INDICADORES_PERMITIDOS:
        raise ValueError(
            f"Indicador no permitido: '{indicador}'. Opciones válidas: {INDICADORES_PERMITIDOS}"
        )

    # 1. Generar variantes de texto limpias (LIMA, Lima, Ica, ICA, Áncash, etc.)
    deptos_variantes = []
    for d in departamentos:
        d_clean = str(d).strip()
        deptos_variantes.extend([
            d_clean,
            d_clean.upper(),
            d_clean.lower(),
            d_clean.capitalize(),
            d_clean.title(),
        ])
        d_lower = d_clean.lower()
        if d_lower in MAPA_DEPARTAMENTOS_TILDES:
            acentuado = MAPA_DEPARTAMENTOS_TILDES[d_lower]
            deptos_variantes.extend([
                acentuado,
                acentuado.upper(),
                acentuado.lower(),
                acentuado.title(),
            ])

    deptos_variantes = list(set(deptos_variantes))
    indicador_upper = indicador_norm.upper()

    # 2. Intentar la consulta para el año especificado
    query = (
        supabase.table(TABLE_NAME)
        .select(f"DEPARTAMENTO,{indicador_upper},ANIO,MES")
        .eq("ANIO", int(anio))
        .in_("DEPARTAMENTO", deptos_variantes)
    )
    res = query.execute()
    data = res.data if res and res.data else []

    # 3. Fallback: Si no hay registros para ese año específico, consultar sin filtro de año
    if not data:
        res_fallback = (
            supabase.table(TABLE_NAME)
            .select(f"DEPARTAMENTO,{indicador_upper},ANIO,MES")
            .in_("DEPARTAMENTO", deptos_variantes)
            .limit(1000)
            .execute()
        )
        data = res_fallback.data if res_fallback else []

    return data