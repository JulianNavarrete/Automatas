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

# Function to ask user to show all the results or just the first 5 and the last 5
def display_user_sessions(user_sessions, is_exercise_one, start_date, end_date):
    if len(user_sessions) <= 15:
        if is_exercise_one == True:
            print("\nSesiones del usuario:")
        else:
            print(f"\nSesiones del usuario entre las fechas {start_date} y {end_date}:")
        
        for session in user_sessions:
            print(session)
    else:
        print(f"Hay {len(user_sessions)} sesiones disponibles para mostrar.")
        choice = input("¿Desea mostrar todas las sesiones (T) o solo las primeras y las últimas 5 (F)? ").lower()
        if choice == "t":
            if is_exercise_one == True:
                print("\nSesiones del usuario:")
            else:
                print(f"\nSesiones del usuario entre las fechas {start_date} y {end_date}:")
            for session in user_sessions:
                print(session)

        elif choice == "f":
            if is_exercise_one == True:
                print("\nPrimeras 5 sesiones del usuario:")
            else:
                print(f"\nPrimeras 5 sesiones del usuario entre las fechas {start_date} y {end_date}:")
            for session in user_sessions[:5]:
                print(session)
    
            if is_exercise_one == True:
                print("\nÚltimas 5 sesiones del usuario:")
            else:
                print(f"\nÚltimas 5 sesiones del usuario entre las fechas {start_date} y {end_date}:")
            for session in user_sessions[-5:]:
                print(session)

        else:
            print("Opción no válida. Mostrando todas las sesiones.")
            if is_exercise_one == True:
                print("\nSesiones del usuario:")
            else:
                print(f"\nSesiones del usuario entre las fechas {start_date} y {end_date}:")
            for session in user_sessions:
                print(session)

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
    total_seconds = sum(int(session[4]) for session in user_sessions)

    # Convert total seconds to days, hours, minutes, and seconds
    days, seconds = divmod(total_seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    return days, hours, minutes, seconds

# Function to obtain the MAC address of a user to identify if they connected with one or multiple devices
def get_user_mac_address(records, user_id):
    user_sessions = [record for record in records if record[1] == user_id]
    mac_addresses = set(session[-1] for session in user_sessions)
    return mac_addresses

# Function to list users connected to an AP based on the AP's MAC address and a specific date or date range
def list_users_connected_to_ap_by_date(records, ap_mac, start_date, end_date):
    connected_users = [record for record in records if record[-2] == ap_mac]
    user_count = {}
    for user in connected_users:
        session_date = user[2]
        if start_date <= session_date <= end_date:
            username = user[1]
            user_count[username] = user_count.get(username, 0) + 1

    return user_count

# Regular expression to validate the format dd/mm/yyyy
def validate_date_format(date):
    pattern = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(2018|2019|2020|2021|2022|2023|2024)$'
    return re.match(pattern, date)

# Regular expression to validate MAC address format for AP
def validate_ap_mac_address(mac):
    pattern = r'^[0-9A-Fa-f]{2}[-][0-9A-Fa-f]{2}[-][0-9A-Fa-f]{2}[-][0-9A-Fa-f]{2}[-][0-9A-Fa-f]{2}[-][0-9A-Fa-f]{2}[:][U][M]$'
    return re.match(pattern, mac)

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
            user_id = input("Ingrese el ID del usuario: ")
            user_sessions = list_sessions_by_user(records, user_id)

            if user_sessions:
                is_exercise_one = True
                display_user_sessions(user_sessions, is_exercise_one, start_date=0, end_date=0)
            else:
                print(f"No se encontraron sesiones para el usuario con ID: {user_id}")


        elif option == '2':
            user_id = input("Ingrese el ID del usuario: ")
            
            # Ask for the start date until the format is valid
            while True:
                start_date = input("Ingrese la fecha de inicio (formato dd/mm/aaaa): ")
                if validate_date_format(start_date):
                    break
                else:
                    print("Formato de fecha incorrecto. Por favor intente de nuevo.")

            # Ask for the end date until the format is valid
            while True:
                end_date = input("Ingrese la fecha de fin (formato dd/mm/aaaa): ")
                if validate_date_format(end_date):
                    break
                else:
                    print("Formato de fecha incorrecto. Por favor intente de nuevo.")
    
            filtered_sessions = list_login_sessions_by_date(records, user_id, start_date, end_date)

            if filtered_sessions:
                is_exercise_one = False
                display_user_sessions(filtered_sessions, is_exercise_one, start_date, end_date)
            else:
                print(f"No se encontraron sesiones para el usuario con ID: {user_id} en el rango de fechas {start_date} a {end_date}")

            '''if filtered_sessions:
                print("Inicios de sesión del usuario en el rango de fechas:")
                for session in filtered_sessions:
                    print(session)
            else:
                print(f"No se encontraron inicios de sesión para el usuario con ID: {user_id}")'''


        elif option == '3':
            user_id = input("Ingrese el ID del usuario: ")
            days, hours, minutes, seconds = total_session_time_by_user(records, user_id)

            print(f"Tiempo total de sesión del usuario con ID {user_id}: {days} días, {hours} horas, {minutes} minutos y {seconds} segundos")


        elif option == '4':
            user_id = input("Ingrese el ID del usuario:  ")
            mac_addresses = get_user_mac_address(records, user_id)
            if mac_addresses:
                print(f"MAC del cliente del usuario con ID {user_id}: {', '.join(mac_addresses)}")
            else:
                print(f"No se encontró información de MAC para el usuario con ID: {user_id}")


        elif option == '5':

            while True:
                ap_mac = input("Ingrese la MAC del AP: ")
                if validate_ap_mac_address(ap_mac):
                    break
                else:
                    print("Formato incorrecto de dirección MAC del AP. Por favor, inténtelo de nuevo.")

            while True:
                start_date = input("Ingrese la fecha de inicio (formato dd/mm/aaaa): ")
                if validate_date_format(start_date):
                    break
                else:
                    print("Formato de fecha incorrecto. Por favor intente de nuevo.")

            while True:
                end_date = input("Ingrese la fecha de fin (formato dd/mm/aaaa): ")
                if validate_date_format(end_date):
                    break
                else:
                    print("Formato de fecha incorrecto. Por favor intente de nuevo.")

            user_count = list_users_connected_to_ap_by_date(records, ap_mac, start_date, end_date)

            if user_count:
                print("Usuarios conectados al AP en el rango de fechas:")
                for username, count in user_count.items():
                    print(f"{username}: {count} veces")
        
            else:
                print(f"No se encontraron usuarios conectados al AP con MAC: {ap_mac}")


        elif option == '0':
            print("¡Hasta luego!")
            break

        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()
