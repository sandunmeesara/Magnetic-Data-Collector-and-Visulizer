import serial
import time

# Replace with your Bluetooth COM port
SERIAL_PORT = "COM10"  # For Windows, e.g., COM5
# SERIAL_PORT = "/dev/tty.your_bluetooth_device"  # For macOS/Linux
BAUD_RATE = 9600
OUTPUT_FILE = "Data.txt"

def read_bluetooth_to_file():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

        try:
            with open(OUTPUT_FILE, "a") as file:
                print(f"Writing data to {OUTPUT_FILE}. Press Ctrl+C to stop.")
                while True:
                    if ser.in_waiting > 0:  # Check if data is available
                        line = ser.readline().decode('utf-8').strip()
                        print(line)  # Display the data in the terminal
                        file.write(line + "\n")  # Write to file
                        file.flush()  # Save data to disk immediately
                    else:
                        time.sleep(0.1)
        except Exception as file_error:
            print(f"Error opening file: {file_error}")

    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
    except serial.SerialException as e:
        print(f"Error: {e}")
    finally:
        if ser.is_open:
            ser.close()
        print("Serial port closed.")


if __name__ == "__main__":
    read_bluetooth_to_file()
