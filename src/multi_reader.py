import pandas as pd
import re
import os

FILE_PATTERN = r'(.*)\.(csv|json|xml)'

class DataFile:
    def __init__(self, data_frame: pd.DataFrame, file_name: str):
        """Constructor de la clase DataFile

        Args:
            data_frame (`pd.DataFrame`): dataframe con la informacion a contener
            file_name (`str`): Nombre base del fichero, con la extension incluida
        """

        (self._file_name, self._file_extension) = re.match(
            pattern = FILE_PATTERN,
            string = file_name
        ).groups()
        self._data_frame = data_frame
        


    def summary(self) -> str:
        """Metodo para obtener un resumen del DataFile. El resumen contiene:
            - Nombre de fichero
            - Numero de registros

        Returns:
            str: Cadena de resumen
        """

        return f'{self._file_name}.{self._file_extension} ({self._data_frame.shape[0]} rows)'



    def content(self) -> str:
        """Metodo que convierte el contenido del dataset en cadena de texto

        Returns:
            str: Cadena de texto resultante
        """

        return self._data_frame.to_string()



    # TODO: Buscar la forma de que el 'subset' resetee el indice
    def filter(self, condition) -> 'DataFile':
        """Metodo para filtrar registros de un DataFile acorde a un predicado
        logico

        Args:
            condition (function): Predicado logico

        Returns:
            DataFile: Nuevo DataFile con los registros filtrados
        """

        subset = self._data_frame[self._data_frame.apply(
            lambda row: condition(row),
            axis = 1
        )]
        return DataFile(subset, f'{self._file_name}.{self._file_extension}')



    def insert(self, value_list: list) -> 'DataFile':
        """Metodo para insertar registros en un DataFile

        Args:
            value_list (list | DataFile): Valor a insertar:
            * Si se trata de un DataFile, realizara una union entre ambos datasets.
            * Si se trata de una lista de tuplas, las insertara de forma secuencial

        Returns:
            DataFile: Nuevo DataFile con los registros actualizados
        """

        new_registers = None
        if type(value_list).__name__ == 'DataFile':
            new_registers = value_list._data_frame
        else:
            new_registers = pd.DataFrame.from_records(
                data = value_list,
                columns = self._data_frame.columns
            )

        return DataFile(
            pd.concat([self._data_frame, new_registers], ignore_index = True),
            f'{self._file_name}.{self._file_extension}'
        )



    def delete(self, condition) -> 'DataFile':
        """Metodo para eliminar registros acorde a un predicado logico

        Args:
            condition (function): Predicado logico

        Returns:
            DataFile: Nuevo DataFile sin los registros eliminados
        """

        new_data_set = self._data_frame[self._data_frame.apply(
            lambda row: not condition(row),
            axis = 1
        )].reset_index(drop = True)

        return DataFile(
            new_data_set,
            f'{self._file_name}.{self._file_extension}'
        )



    def update(self, condition, statement) -> 'DataFile':
        """Metodo para actualizar registros acorde a un predicado logico,
        aplicando una funcion de cambio (accion) a cada registro afectado

        Args:
            condition (function): Predicado logico
            statement (function): Funcion que describa los cambios a realizar
            a cada fila

        Returns:
            DataFile: Nuevo DataFile con los registros actualizados
        """

        new_data_set = self._data_frame.copy(deep = True)
        for index, row in new_data_set.iterrows():
            if condition(row):
                statement(row)
                new_data_set.iloc[index] = row
        
        return DataFile(
            new_data_set,
            f'{self._file_name}.{self._file_extension}'
        )
        


    def add_field(self, field_name: str, expression = None) -> 'DataFile':
        """Metodo para añadir un campo nuevo al dataset

        Args:
            field_name (str): Nombre del campo a añadir
            expression (Any | function, optional): Valor por defecto a escribir
            en el nuevo campo.
            Si en una funcion, el resultado de dicha funcion
            para cada fila se guardara en el campo. Defaults to None.

        Returns:
            DataFile: Nuevo DataFile con el nuevo campo insertado
        """

        new_data_set = self._data_frame.copy(deep = True)
        if type(expression).__name__ == 'function':
            new_data_set[field_name] = expression(new_data_set)
        else:
            new_data_set[field_name] = expression

        return DataFile(
            new_data_set,
            f'{self._file_name}.{self._file_extension}'
        )
        
    

    def drop_field(self, field_name: str) -> 'DataFile':
        """Metodo para eliminar un campo ya existente del dataset

        Args:
            field_name (str): Nombre del campo a eliminar

        Returns:
            DataFile: Nuevo DataFile sin el campo eliminado
        """

        new_data_set = self._data_frame.drop(columns = [field_name])
        return DataFile(
            new_data_set,
            f'{self._file_name}.{self._file_extension}'
        )



    def write(self, file_path: str) -> None:
        """Metodo para guardar el contenido del DataFile en un fichero

        Args:
            file_path (str): Ruta del fichero en el que guardar el DataFile
        """

        base_name = os.path.basename(file_path)
        _, extension = re.match(
            pattern = FILE_PATTERN,
            string = base_name
        ).groups()
        match extension:
            case 'csv':
                self._data_frame.to_csv(file_path)
            case 'xml':
                self._data_frame.to_xml(file_path)
            case 'json':
                self._data_frame.to_json(file_path)



def read_csv(file_path: str) -> DataFile:
    """Funcion para leer un fichero en formato .csv y guardar su contenido en un
    objeto DataFile

    Args:
        file_path (str): Ruta del fichero a leer

    Returns:
        DataFile: DataFile con la información contenida
    """

    return _read_file(file_path, pd.read_csv)



def read_xml(file_path: str) -> DataFile:
    """Funcion para leer un fichero en formato .xml y guardar su contenido en un
    objeto DataFile

    Args:
        file_path (str): Ruta del fichero a leer

    Returns:
        DataFile: DataFile con la información contenida
    """

    return _read_file(file_path, pd.read_xml)



def read_json(file_path: str) -> DataFile:
    """Funcion para leer un fichero en formato .json y guardar su contenido en un
    objeto DataFile

    Args:
        file_path (str): Ruta del fichero a leer

    Returns:
        DataFile: DataFile con la información contenida
    """

    return _read_file(file_path, pd.read_json)



def _read_file(file_path: str, parsing_function) -> DataFile:
    """Funcion invocada por las funciones de lectura de ficheros de datos para
    procesar la lectura de ficheros

    Args:
        file_path (str): Ruta del fichero a leer
        parsing_function (function): Función de parsing a aplicar al fichero

    Raises:
        Exception: El formato del fichero no concuerda con el esperado o el
        fichero no existe

    Returns:
        DataFile: DataFile con la información contenida
    """
    try:
        data_frame = parsing_function(file_path)
        file_name = os.path.basename(file_path)
        return DataFile(data_frame, file_name)
    except Exception:
        raise Exception("Incorrect file format")