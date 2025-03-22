import pyreadstat
import os


def convert_sav_to_csv(sav_file_path):
    try:
        df, meta = pyreadstat.read_sav(sav_file_path)
        
        csv_file_path = os.path.splitext(sav_file_path)[0] + '.csv'

        df.to_csv(csv_file_path, index=False)
        
        print(f'Archivo convertido con éxito. Archivo guardado en: {csv_file_path}')
    except Exception as e:
        print(f'Ocurrió un error al convertir el archivo: {e}')


def main():
    sav_file_name = input('Ingresa el nombre del archivo .sav (incluye la extensión .sav): ')


    sav_file_path = os.path.join(os.getcwd(), sav_file_name)


    convert_sav_to_csv(sav_file_path)


if __name__ == "__main__":
    main()