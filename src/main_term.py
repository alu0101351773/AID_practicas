from multi_reader import *
import re


global_dataset: DataFile = None


log_operator_dict = {
    "eq": lambda field, value: lambda row: row[field] == value,
    "ne": lambda field, value: lambda row: row[field] != value,
    "lt": lambda field, value: lambda row: row[field] <  value,
    "le": lambda field, value: lambda row: row[field] <= value,
    "gt": lambda field, value: lambda row: row[field] >  value,
    "ge": lambda field, value: lambda row: row[field] >= value
}

def is_float(value):
    try:
        float(value)
    except:
        return False
    else:
        return True


def read_data_file():
    global global_dataset
    user_selection = input("Nombre de fichero de datos: ").strip()
    file_extension = input("Formato de fichero (csv, json, xml): ").strip()
    match file_extension:
        case "csv":
            global_dataset = read_csv(user_selection)
        case "json":
            global_dataset = read_json(user_selection)
        case "xml":
            global_dataset = read_xml(user_selection)
        case _:
            raise Exception(f"Formato de fichero no soportado: .{file_extension}")


def show_file_summary():
    global global_dataset
    print(f"\nResumen de fichero: {global_dataset.summary()}\n")


def show_file_content():
    global global_dataset
    print(f"\nContenido del fichero:\n{global_dataset.content()}\n")


def filter_file():
    global global_dataset

    file_field = input("Campo a filtrar: ").strip()
    
    file_value = input("Valor a filtrar: ").strip()
    if str.isnumeric(file_value):
        file_value = int(file_value)
    elif is_float(file_value):
        file_value = float(file_value)
    
    print("""
        Formato de operadores de comparación:
            - eq: campo == valor
            - ne: campo != valor
            - gt: campo >  valor
            - ge: campo >= valor
            - lt: campo <  valor
            - le: campo <= valor
    """)
    logical_operator = input("Operador de comparación: ").strip()
    if logical_operator not in ["eq", "ne", "gt", "ge", "lt", "le"]:
        raise Exception("Operador de comparación desconocido")
    
    filter_condition = log_operator_dict[logical_operator](file_field, file_value)
    global_dataset = global_dataset.filter(filter_condition)


def main_menu():
    print("""
        Seleccione la operación a realizar:
          
            1. Leer fichero
            2. Mostrar resumen
            3. Mostrar contenido
            4. Filtrar por contenido
            5. Insertar filas
            6. Eliminar filas
            7. Modificar filas
            8. Añadir columna
            9. Eliminar columna
           10. Almacenar los cambios en fichero
          
           -1. Salida del programa
    """)
    user_selection = int(input("Código de operación: ").strip())

    match user_selection:
        case 1:
            read_data_file()
        case 2:
            pass
        case 3:
            pass
        case 4:
            pass
        case 5:
            pass
        case 6:
            pass
        case 7:
            pass
        case 8:
            pass
        case 9:
            pass
        case 10:
            pass
        case -1:
            pass
        case _:
            raise Exception("Opción inválida")


if __name__ == "__main__":
    read_data_file()
    show_file_content()

    filter_file()
    show_file_content()