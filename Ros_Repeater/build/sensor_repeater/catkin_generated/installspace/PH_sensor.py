import serial
import time

# Configure the serial port
ser = serial.Serial(
    port='COM1',       # Replace with your serial port
    baudrate=9600,     # Replace with the correct baud rate
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1          # Set a timeout for reading
)

# Hex command to send (as shown in the image)
hex_command = '0103000000240b'

# Convert the hex command to bytes
command_bytes = bytes.fromhex(hex_command)

# Send the command
ser.write(command_bytes)

# Wait for a response
time.sleep(1)

# Read the response
response = ser.read(ser.inWaiting())

# Close the serial port
ser.close()

# Print the response in hexadecimal format
print("Response:", response.hex())

# If you need to process the response further, you can do so here
# For example, converting to integers or decoding text
