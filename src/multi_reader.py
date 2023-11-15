import pandas as pd
import re
import os

FILE_PATTERN = r'(.*)\.(csv|json|xml)'

class DataFile:
    def __init__(self, data_frame: pd.DataFrame, file_name: str):
        (self._file_name, self._file_extension) = re.match(
            pattern = FILE_PATTERN,
            string = file_name
        ).groups()
        self._data_frame = data_frame
        

    def summary(self) -> str:
        return f'{self._file_name}.{self._file_extension} ({self._data_frame.shape[0]} rows)'


    def content(self) -> str:
        return self._data_frame.to_string()


    def filter(self, condition) -> 'DataFile':
        subset = self._data_frame[self._data_frame.apply(
            lambda row: condition(row),
            axis = 1
        )]
        return DataFile(subset, f'{self._file_name}.{self._file_extension}')


    def insert(self, value_list: list) -> 'DataFile':
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
        new_data_set = self._data_frame[self._data_frame.apply(
            lambda row: not condition(row),
            axis = 1
        )].reset_index(drop = True)

        return DataFile(
            new_data_set,
            f'{self._file_name}.{self._file_extension}'
        )


    def update(self, condition, statement) -> 'DataFile':
        new_data_set = self._data_frame.copy(deep = True)
        for index, row in new_data_set.iterrows():
            if condition(row):
                statement(row)
                new_data_set.iloc[index] = row
        
        return DataFile(
            new_data_set,
            f'{self._file_name}.{self._file_extension}'
        )
        

    def add_field(self, field_name, expression = None) -> 'DataFile':
        new_data_set = self._data_frame.copy(deep = True)
        if type(expression).__name__ == 'function':
            new_data_set[field_name] = expression(new_data_set)
        else:
            new_data_set[field_name] = expression

        return DataFile(
            new_data_set,
            f'{self._file_name}.{self._file_extension}'
        )
        
    
    def drop_field(self, field_name) -> 'DataFile':
        new_data_set = self._data_frame.drop(columns = [field_name])
        return DataFile(
            new_data_set,
            f'{self._file_name}.{self._file_extension}'
        )


    def write(self, file_path) -> None:
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