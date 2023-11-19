from multi_reader import *
import os


global_dataset: DataFile = None


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


def parse_filter_condition():
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
    logical_operator = input("Operador de comparación: ").strip().lower()
    if logical_operator not in ["eq", "ne", "gt", "ge", "lt", "le"]:
        raise Exception("Operador de comparación desconocido")
    
    operator_dict = {
        "eq": lambda row: row[file_field] == file_value,
        "ne": lambda row: row[file_field] != file_value,
        "gt": lambda row: row[file_field] >  file_value,
        "ge": lambda row: row[file_field] >= file_value,
        "lt": lambda row: row[file_field] <  file_value,
        "le": lambda row: row[file_field] <= file_value,
    }

    return operator_dict[logical_operator]


def filter_file():
    global global_dataset
    global_dataset = global_dataset.filter(parse_filter_condition())


def insert_rows():
    global global_dataset

    row_number = int(input("Número de filas a insertar: "))
    new_rows = [ [] for i in range(row_number)]
    for i in range(row_number):
        
        for field in global_dataset.columns():
            field_value = input(f"Valor de la columna \"{field}\": ")
            
            if str.isnumeric(field_value):
                field_value = int(field_value)
            elif is_float(field_value):
                field_value = float(field_value)
        
            new_rows[i].append(field_value)
    
    global_dataset = global_dataset.insert(new_rows)


def delete_rows():
    global global_dataset
    filter_condition = parse_filter_condition()
    rows_to_be_removed: DataFile = global_dataset.filter(filter_condition)
    print(f"Filas a ser eliminadas:\n{rows_to_be_removed.content()}\n")
    user_decision = input("¿Desea eliminar estas filas? [y], [n]: ").strip().lower()

    match user_decision:
        case 'y':
            global_dataset = global_dataset.delete(filter_condition)
        case 'n':
            pass
        case _:
            raise Exception("Decisión inválida")


def parse_update_action():
    file_field = input("Campo a actualizar: ").strip()
    file_value = input("Valor a actualizar: ").strip()

    if str.isnumeric(file_value):
        file_value = int(file_value)
    elif is_float(file_value):
        file_value = float(file_value)
    
    def action(row):
        row[file_field] = file_value

    return action


def update_rows():
    global global_dataset
    update_condition = parse_filter_condition()
    update_action = parse_update_action()
    
    pre_update_dataset = global_dataset.filter(update_condition)
    print(f"Filas antes de ser modificadas:\n{pre_update_dataset.content()}\n")

    pre_update_dataset = pre_update_dataset.update(
        update_condition,
        update_action
    )
    print(f"Filas después de ser modificadas:\n{pre_update_dataset.content()}\n")
    
    user_decision = input("¿Desea actualizar estas filas? [y], [n]: ").strip().lower()
    match user_decision:
        case 'y':
            global_dataset = global_dataset.update(
                update_condition,
                update_action
            )
        case 'n':
            pass
        case _:
            raise Exception("Decisión inválida")


def add_field():
    global global_dataset

    file_field = input("Campo a añadir: ").strip()
    file_value = input("Valor a añadir: ").strip()

    if str.isnumeric(file_value):
        file_value = int(file_value)
    elif is_float(file_value):
        file_value = float(file_value)

    global_dataset = global_dataset.add_field(file_field, file_value)


def drop_field():
    global global_dataset

    file_field = input("Campo a eliminar: ").strip()
    global_dataset = global_dataset.drop_field(file_field)


def save_to_file():
    global global_dataset

    file_path = input("Fichero destino: ").strip()
    global_dataset.write(file_path)


def main_menu():
    while True:
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
        os.system('cls' if os.name == 'nt' else 'clear')

        match user_selection:
            case 1:
                read_data_file()
            case 2:
                show_file_summary()
            case 3:
                show_file_content()
            case 4:
                filter_file()
                show_file_content()
            case 5:
                insert_rows()
                show_file_content()
            case 6:
                delete_rows()
                show_file_content()
            case 7:
                update_rows()
                show_file_content()
            case 8:
                add_field()
                show_file_content()
            case 9:
                drop_field()
                show_file_content()
            case 10:
                save_to_file()
            case -1:
                exit(0)
            case _:
                raise Exception("Opción inválida")


if __name__ == "__main__":
    main_menu()