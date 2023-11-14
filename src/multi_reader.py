import pandas as pd

class DataFile:
    # TODO: Constructor que reciba un pd.dataframe y su nombre
        # * Debe guardar el dataframe, el nombre y la extension
    def __init__(self, dataframe: pd.Dataframe, file_name: str):
        pass

    # TODO: Metodo para mostrar en pantalla nombre completo de fichero
    # y numero de registros

    # TODO: Metodo de filtro que reciba una funcion
    # y retorne un DataFile con ese contenido

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
    pass


def read_xml(file_path: str) -> DataFile:
    pass


def read_json(file_path: str) -> DataFile:
    pass