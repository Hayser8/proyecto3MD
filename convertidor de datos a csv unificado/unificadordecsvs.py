import pandas as pd
import os


def unir_csvs(csvs_paths: list, output_path: str):
    columnas_renombradas = {
        'numero_corre': 'id_registro',
        'núm_corre': 'id_registro',
        'día_ocu': 'dia_ocu',
        'día_sem_ocu': 'dia_sem_ocu',
        'sexo_per': 'sexo',
        'sexo_dete': 'sexo',
        'edad_per': 'edad',
        'edad_dete': 'edad',
        'delito_com': 'delito',
        'delito_infringido': 'delito',
        'área_geo_ocu': 'area_geo_ocu',
        'areag_ocu': 'area_geo_ocu',
        'agrea_ocu': 'area_geo_ocu',
        'g_hora_mañ.tar.noch': 'g_hora_periodo',
        'cód_int_Detenidos': 'codigo_interno'
    }


    dfs = []

    for path in csvs_paths:
        df = pd.read_csv(path)
        
        df.rename(columns=columnas_renombradas, inplace=True)

        if '2011.csv' in path:
            df['año_ocu'] = 2011
        elif '2012.csv' in path:
            df['año_ocu'] = 2012


        dfs.append(df)


    df_unificado = pd.concat(dfs, ignore_index=True)

    df_unificado.to_csv(output_path, index=False)

    print(f"CSV unificado guardado exitosamente en: {output_path}")


csvs_paths = ['2024.csv', '2023.csv', '2022.csv', '2021.csv', '2020.csv', '2019.csv', '2018.csv', '2017.csv', '2016.csv', '2012.csv', '2011.csv']
output_path = 'todoscsvs.csv'
unir_csvs(csvs_paths, output_path)
