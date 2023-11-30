import pandas as pd
from datetime import datetime
import numpy as np

class JsonNormalizer:
    def __init__(self) -> None:
        pass


    def normalize(self, raw_data) -> pd.DataFrame:
        self._normalized_data = pd.DataFrame(columns = [
            "DNI",
            "Nombre",
            "Apellidos",
            "Ciudad_residencia",
            "Fecha_nacimiento",
            "Sexo",
            "Estatura",
            "Aficiones",
            "Amigos"
        ])

        self._normalize_dni(raw_data)
        self._normalize_name(raw_data)
        self._normalize_surname(raw_data)
        self._normalize_city(raw_data)
        self._normalize_birthdate(raw_data)
        self._normalize_sex(raw_data)
        self._normalize_height()
        self._normalize_hobbies(raw_data)
        self._normalize_friend_list(raw_data)

        return self._normalized_data

    
    def _normalize_dni(self, raw_data) -> None:
        self._normalized_data['DNI'] = raw_data['DNI']


    def _normalize_name(self, raw_data) -> None:
        self._normalized_data['Nombre'] = raw_data['Nombre']


    def _normalize_surname(self, raw_data) -> None:
        self._normalized_data['Apellidos'] = raw_data['Apellidos']


    def _normalize_city(self, raw_data) -> None:
        self._normalized_data['Ciudad_residencia'] = raw_data['Ciudad']


    def _normalize_birthdate(self, raw_data) -> None:
        def convert_age(source_age):
            if np.isnan(source_age):
                return np.nan
            else:
                today = datetime.now()
                return f'{today.day:02d}-{today.month:02d}-{today.year - int(source_age)}'
            
        self._normalized_data['Fecha_nacimiento'] = raw_data['Edad'].apply(convert_age)


    def _normalize_sex(self, raw_data) -> None:
        self._normalized_data['Sexo'] = raw_data['Sexo']


    def _normalize_height(self) -> None:
        self._normalized_data['Estatura'] = 0


    def _normalize_hobbies(self, raw_data) -> None:
        def hobbies_normalization(value):
            if not isinstance(value, list):
                return []
            else:
                return list(set(value))

        self._normalized_data['Aficiones'] = raw_data['Aficiones'].apply(hobbies_normalization)


    def _normalize_friend_list(self, raw_data) -> None:
        def friends_normalization(value):
            if not isinstance(value, list):
                return []
            else:
                return list({friend.get('DNI') for friend in value})

        self._normalized_data['Amigos'] = raw_data['Amigos'].apply(friends_normalization)
        