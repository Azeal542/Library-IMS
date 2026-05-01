import csv
from pathlib import Path
import API
import json
import os, random, string
import time
import serial_reader


#input_folder = Path.home() / "Downloads"
input_folder = ("C:\\Users\\CalebPierce\\OneDrive - Klamath Family Head Start\\Documents\\Downloads")
input_file = (input_folder + "\\exportUsers.csv")
global users
users = []
global add
add = []


def password_generator():
    length = 13
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed = (os.urandom(1024))
    password = (''.join(random.choice(chars) for i in range(length)))
    print(f"Generated password: {password}")
    return password

def import_users():
    #with open('output.csv', mode='w', newline='') as outputfile:
        with open(input_file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["userPrincipalName"]:
                    if "onmicrosoft.com" not in row["userPrincipalName"]:
                        addrow = [row[list(row.keys())[1]], row[list(row.keys())[2]]]
                        users.append(addrow)
                        #outputfile.write(f"{addrow[0]},{addrow[1]}\n")
            
def check_users():
    for user in users:
        try:
            time.sleep(0.5)  # Sleep for 0.5 seconds to avoid hitting API rate limits
            result = API.get_User_By_Email(user[1])
            jResult = json.loads(result)
            if jResult["total"] > 0:
                print(f"User {user[0]} with email {user[1]} already exists in Snipe-IT.")
            else:
                add.append(user)
                print(f"User {user[0]} with email {user[1]} does not exist in Snipe-IT and will be added.")
        except Exception as e:
            print(f"An error occurred while checking user {user[0]} with email {user[1]}: {e}")

def create_users():
    scanned_ids = set()
    for user in add:
        time.sleep(0.5)  # Sleep for 0.5 seconds to avoid hitting API rate limits
        print(f"Creating user {user[0]} with email {user[1]} in Snipe-IT.")
        first_name = str(user[0].split()[0])
        last_name = str(user[0].split()[-1])
        email = str(user[1])
        password = str(password_generator())
        username = str(user[0])
        while True:  # Loop until a unique ID is scanned
            id = serial_reader.read_serial_data()
            if id in scanned_ids:
                print(f"ID {id} has already been scanned. Please scan again.")
            else:
                scanned_ids.add(id)
                print(f"Received ID: {id}")
                break  # Exit the loop if the ID is unique
        print(f"Received ID: {id}")
        employee_num = id
        
        #print(first_name, username, password, last_name, email, employee_num)
        API.create_user(first_name, username, password, last_name, email, employee_num)

if __name__ == "__main__":
    import_users()
    check_users()
    create_users()