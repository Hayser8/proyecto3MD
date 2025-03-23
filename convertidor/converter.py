import pyreadstat
import os


def convert_sav_to_csv(sav_file_path):
    try:
        # Leer el archivo .sav usando pyreadstat
        df, meta = pyreadstat.read_sav(sav_file_path)
        
        # Generar la ruta del archivo CSV con el mismo nombre que el archivo .sav
        csv_file_path = os.path.splitext(sav_file_path)[0] + '.csv'

        # Guardar el DataFrame como CSV
        df.to_csv(csv_file_path, index=False)
        
        print(f'Archivo convertido con éxito. Archivo guardado en: {csv_file_path}')
    except Exception as e:
        print(f'Ocurrió un error al convertir el archivo: {e}')


def main():
    # Nombre del archivo .sav que se encuentra en la misma carpeta
    sav_file_name = input('Ingresa el nombre del archivo .sav (incluye la extensión .sav): ')

    # Obtener la ruta del archivo .sav en la misma carpeta que el script
    sav_file_path = os.path.join(os.getcwd(), sav_file_name)

    # Convertir el archivo
    convert_sav_to_csv(sav_file_path)


if __name__ == "__main__":
    main()