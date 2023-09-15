import re


# Function to load the file and extract the records
def load_records(file_name):
    try:
        with open(file_name, 'r') as file:
            content = file.read()
        # Split the content into lines and remove the header line
        lines = content.strip().split('\n')[1:]
        # Split each line into fields using ';'
        records = [line.split(';') for line in lines]
        return records
    except FileNotFoundError:
        print(f"El archivo '{file_name}' no fue encontrado.")
        return []

# Function to list all sessions of a user based on their ID
def list_sessions_by_user(records, user_id):
    user_sessions = [record for record in records if record[1] == user_id]
    return user_sessions

# Function to list login sessions of a user within a specific date range
def list_login_sessions_by_date(records, user_id, start_date, end_date):
    user_sessions = [record for record in records if record[1] == user_id]
    filtered_sessions = []
    for session in user_sessions:
        session_date = session[2]
        if start_date <= session_date <= end_date:
            filtered_sessions.append(session)
    return filtered_sessions

# Function to calculate the total session time of a user
def total_session_time_by_user(records, user_id):
    user_sessions = [record for record in records if record[1] == user_id]
    total_time = sum(int(session[4]) for session in user_sessions)
    return total_time

# Function to obtain the MAC address of a user to identify if they connected with one or multiple devices
def get_user_mac_address(records, user_id):
    user_sessions = [record for record in records if record[1] == user_id]
    mac_addresses = set(session[-1] for session in user_sessions)
    return mac_addresses

# Function to list users connected to an AP based on the AP's MAC address and a specific date or date range
def list_users_connected_to_ap_by_date(records, ap_mac, start_date, end_date):
    connected_users = [record for record in records if record[-2] == ap_mac]
    filtered_users = []
    for user in connected_users:
        session_date = user[2]
        if start_date <= session_date <= end_date:
            filtered_users.append(user[1])
    return filtered_users

# Regular expression to validate the format dd/mm/yyyy
def validate_date_format(date):
    pattern = r'^\d{2}/\d{2}/\d{4}$'
    return re.match(pattern, date)

# Function to display the menu and get the user's option
def show_menu():
    print("\n--- Menú de Informes ---")
    print("1. Listar todas las sesiones de un usuario mediante su ID.")
    print("2. Listar los inicios de sesión en un usuario en un periodo de tiempo determinado.")
    print("3. Tiempo total de la sesión de un usuario.")
    print("4. MAC de un usuario, para identificar si se conectó con un dispositivo o varios.")
    print("5. Listar los usuarios conectados a un AP mediante la MAC del AP en una determinada fecha o rango de fecha.")
    print("0. Salir")

    option = input("Seleccione una opción: ")
    return option

# Main function of the program
def main():
    records = load_records("usuarios_wifi.txt")

    while True:
        option = show_menu()

        if option == '1':
            user_id = input("Ingrese el ID del usuario:  ")
            user_sessions = list_sessions_by_user(records, user_id)
            if user_sessions:
                print("Sesiones del usuario:")
                for session in user_sessions:
                    print(session)
            else:
                print(f"No se encontraron sesiones para el usuario con ID: {user_id}")

        elif option == '2':
            user_id = input("Ingrese el ID del usuario: ")
            start_date = input("Ingrese la fecha de inicio (formato dd/mm/aaaa): ")
            end_date = input("Ingrese la fecha de fin (formato dd/mm/aaaa): ")
            filtered_sessions = list_login_sessions_by_date(records, user_id, start_date, end_date)
            if filtered_sessions:
                print("Inicios de sesión del usuario en el rango de fechas:")
                for session in filtered_sessions:
                    print(session)
            else:
                print(f"No se encontraron inicios de sesión para el usuario con ID: {user_id}")

        elif option == '3':
            user_id = input("Ingrese el ID del usuario:  ")
            total_time = total_session_time_by_user(records, user_id)
            print(f"Tiempo total de sesión del usuario con ID {user_id}: {total_time} minutos")

        elif option == '4':
            user_id = input("Ingrese el ID del usuario:  ")
            mac_addresses = get_user_mac_address(records, user_id)
            if mac_addresses:
                print(f"MAC del cliente del usuario con ID {user_id}: {', '.join(mac_addresses)}")
            else:
                print(f"No se encontró información de MAC para el usuario con ID: {user_id}")

        elif option == '5':
            ap_mac = input("Ingrese la MAC del AP: ")
            start_date = input("Ingrese la fecha de inicio (formato dd/mm/aaaa): ")
            end_date = input("Ingrese la fecha de fin (formato dd/mm/aaaa): ")
            connected_users = list_users_connected_to_ap_by_date(records, ap_mac, start_date, end_date)
            if connected_users:
                print("Usuarios conectados al AP en el rango de fechas:")
                for user in connected_users:
                    print(user)
            else:
                print(f"No se encontraron usuarios conectados al AP con MAC: {ap_mac}")

        elif option == '0':
            print("¡Hasta luego!")
            break

        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    main()
