import pandas as pd
import re
import os

FILE_PATTERN = r'(.*)\.(csv|json|xml)'

class DataFile:
    def __init__(self, data_frame: pd.DataFrame, file_name: str):
        (self.file_name, self.file_extension) = re.match(
            pattern = FILE_PATTERN,
            string = file_name
        ).groups()
        self.data_frame = data_frame
        

    def summary(self) -> str:
        return f'{self.file_name}.{self.file_extension} ({self.data_frame.shape[0]} rows)'


    def filter(self, filter_function):
        subset = self.data_frame[self.data_frame.apply(
            lambda row: filter_function(row),
            axis = 1
        )]
        return DataFile(subset, f'{self.file_name}.{self.file_extension}')

    # TODO: Metodos de manipulacion de datos como:
    # - Insertar registros
    # - Borrar registros acorde a un filtro (funcion)
    # - Actualizar valores de... un update, chico

    # TODO: Metodo para modificar el schema de la estructura de datos para:
    # - Añadir campos
    # - Eliminar campos

    # TODO: Metodo para guardar los datos en un fichero (por defecto se 
    # utilizara) el mismo formato del original, pero se puede especificar
    pass


def read_csv(file_path: str) -> DataFile:
    return _read_file(file_path, pd.read_csv)


def read_xml(file_path: str) -> DataFile:
    return _read_file(file_path, pd.read_xml)


def read_json(file_path: str) -> DataFile:
    return _read_file(file_path, pd.read_json)


def _read_file(file_path: str, parsing_function) -> DataFile:
    try:
        data_frame = parsing_function(file_path)
        file_name = os.path.basename(file_path)
        return DataFile(data_frame, file_name)
    except Exception:
        raise Exception("Incorrect file format")