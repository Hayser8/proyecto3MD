import os
import glob
import pandas as pd

def unir_csvs(csv_paths: list[str], output_path: str):
    columnas_renombradas = {
        # Fecha del hecho
        'HEC_DIA': 'dia_ocurrencia',
        'HEC_MES': 'mes_ocurrencia',
        'HEC_ANO': 'anio_ocurrencia',
        'HEC_DEPTOMCPIO': 'dep_municipio_ocurrencia',
        'HEC_DEPTO': 'dep_municipio_ocurrencia',
        'HEC_AREA': 'area_ocurrencia',
        'HEC_TIPAGRE': 'tipo_agresion',
        'HEC_RECUR_DENUN': 'reiteracion_denuncia',

        # Fecha de registro/denuncia
        'DIA_EMISION': 'dia_registro',
        'MES_EMISION': 'mes_registro',
        'ANO_EMISION': 'anio_registro',

        # Ubicación registro
        'DEPTO_MCPIO': 'dep_municipio_registro',
        'DEPTO': 'departamento_registro',

        # Folio interno
        'NUMERO_BOLETA': 'numero_boleta',

        # Quién reporta
        'QUIEN_REPORTA': 'quien_reporta',

        # Víctima
        'VIC_SEXO': 'sexo_victima',
        'VIC_EDAD': 'edad_victima',
        'TOTAL_HIJOS': 'total_hijos_victima',
        'NUM_HIJ_HOM': 'hijos_hombres_victima',
        'NUM_HIJ_MUJ': 'hijas_mujeres_victima',
        'VIC_ALFAB': 'alfabeta_victima',
        'VIC_ESCOLARIDAD': 'escolaridad_victima',
        'VIC_EST_CIV': 'estado_civil_victima',
        'VIC_GRUPET': 'pueblo_victima',
        'VIC_NACIONAL': 'nacionalidad_victima',
        'VIC_TRABAJA': 'trabaja_victima',
        'VIC_OCUP': 'ocupacion_victima',
        'VIC_DEDICA': 'dedica_victima',
        'VIC_DISC': 'discapacidad_victima',
        'TIPO_DISCAQ': 'tipo_discapacidad_victima',
        'VIC_REL_AGR': 'relacion_victima_agresor',
        'OTRAS_VICTIMAS': 'otras_victimas_total',
        'VIC_OTRAS_HOM': 'otras_victimas_hombres',
        'VIC_OTRAS_MUJ': 'otras_victimas_mujeres',
        'VIC_OTRAS_N_OS': 'otras_victimas_ninos',
        'VIC_OTRAS_N_AS': 'otras_victimas_ninas',

        # Agresor
        'AGR_SEXO': 'sexo_agresor',
        'AGR_EDAD': 'edad_agresor',
        'AGR_ALFAB': 'alfabeta_agresor',
        'AGR_ESCOLARIDAD': 'escolaridad_agresor',
        'AGR_EST_CIV': 'estado_civil_agresor',
        'AGR_GRUPET': 'pueblo_agresor',
        'AGR_NACIONAL': 'nacionalidad_agresor',
        'AGR_TRABAJA': 'trabaja_agresor',
        'AGR_OCUP': 'ocupacion_agresor',
        'AGR_DEDICA': 'dedica_agresor',
        'AGRESORES_OTROS_TOTAL': 'otros_agresores_total',
        'OTROS_AGRESORES': 'otros_agresores_total',
        'AGR_OTROS_HOM': 'otros_agresores_hombres',
        'AGR_OTRAS_MUJ': 'otros_agresores_mujeres',
        'AGR_OTROS_N_OS': 'otros_agresores_ninos',
        'AGR_OTRAS_N_AS': 'otros_agresores_ninas',

        # Institución que registra
        'INST_DENUN_HECHO': 'institucion_registro',
        'INST_DONDE_DENUNCIO': 'institucion_denuncia_previa',
        'ORGANISMO_JURISDICCIONAL': 'organismo_jurisdiccional',
        'CONDUCENTE': 'conducente',
        'LEY_APLICABLE': 'ley_aplicable',
        'MEDIDAS_SEGURIDAD': 'medidas_seguridad',
        'TIPO_MEDIDA': 'tipo_medida',
        'ORGANISMO_REMITE': 'organismo_remite'
    }

    dfs = []
    for path in csv_paths:
        df = pd.read_csv(path, low_memory=False)
        df.rename(columns=columnas_renombradas, inplace=True)
        df.drop(columns=['filter_$'], errors='ignore', inplace=True)
        df.drop(columns=[c for c in df.columns if c.startswith('ARTICULOVIF')], errors='ignore', inplace=True)
        df = df.loc[:, ~df.columns.duplicated()]
        dfs.append(df)

    if not dfs:
        print("❌ No hay archivos CSV para concatenar.")
        return

    resultado = pd.concat(dfs, ignore_index=True)
    resultado.to_csv(output_path, index=False)
    print(f"✅ CSV unificado guardado en: {output_path}")

if __name__ == "__main__":
    carpeta = os.getcwd()
    rutas = glob.glob(os.path.join(carpeta, "*vif.csv"))
    print("📂 Directorio actual:", carpeta)
    print("🔍 Archivos encontrados:", rutas)
    unir_csvs(rutas, "todoscsvs.csv")
