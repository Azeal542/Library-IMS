import serial
import csv

# Configure the serial port (adjust port and baud rate)
#ser = serial.Serial('/dev/ttyACM0', 9600)  # Linux/Mac
ser = serial.Serial('COM12', 9600)       # Windows

def read_serial_data():
    try:
        while True:
            # Read a line from the serial port
            line = ser.readline()
            if line:
                # Decode bytes to string and remove newline characters
                data = line.decode('utf-8').strip()
                print(data)
                return data
    except KeyboardInterrupt:
        ser.close()   
        
def import_assets():
    scanned_ids = set()
    repeat = int(input("How many assets do you want to add? "))
    for i in range(repeat):
        user_input = input(f"Enter name of asset {i+1}: ")
        print(f"Reading serial data for asset: {user_input}")
        while True:  # Loop until a unique ID is scanned
            id = read_serial_data()
            if id in scanned_ids:
                print(f"ID {id} has already been scanned. Please scan again.")
            else:
                scanned_ids.add(id)
                print(f"Received ID: {id}")
                break  # Exit the loop if the ID is unique
        print(f"Received ID: {id}")
        with open('assets.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Check if the file is empty to write headers
                writer.writerow(['ID', 'Asset Name', 'Asset Tag'])
            writer.writerow([id, user_input, f"book_{id}"])

if __name__ == "__main__":
    import_assets()