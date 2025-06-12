import serial
import csv
import time

# port and baud
PORT = '/dev/cu.usbserial-210'
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)  # ESP32 reset time

# open CSV file for writing
from datetime import datetime
filename = datetime.now().strftime("power_log_%Y-%m-%d_%H-%M-%S.csv")
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Timestamp', 'Voltage (V)', 'Current (A)', 'Power (W)'])

    print("Logging started. Press Ctrl+C to stop.")

    try:
        while True:
            line = ser.readline().decode().strip()
            if "Voltage RMS" in line:
                voltage = float(line.split(":")[1].strip())
                current = float(ser.readline().decode().split(":")[1].strip())
                power = float(ser.readline().decode().split(":")[1].strip())

                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([timestamp, voltage, current, power])
                csvfile.flush()
                print(f"[{timestamp}] V={voltage}V  I={current}A  P={power}W")

    except KeyboardInterrupt:
        print("Logging stopped.")
        ser.close()
