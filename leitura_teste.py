import time
import spidev
import RPi.GPIO as GPIO

# Constants
local_address = 0xBA
destination = 0xBC
msg_count = 0
interval = 5  # Interval in seconds

# SPI configuration
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000

# GPIO configuration
reset_pin = 25
cs_pin = 8
irq_pin = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(reset_pin, GPIO.OUT)
GPIO.setup(cs_pin, GPIO.OUT)
GPIO.setup(irq_pin, GPIO.IN)

# Function to send a LoRa message
def send_message(outgoing):
    GPIO.output(cs_pin, GPIO.LOW)
    spi.xfer2([destination, local_address, msg_count, len(outgoing)] + list(outgoing.encode('utf-8')))
    GPIO.output(cs_pin, GPIO.HIGH)

def on_receive(payload):
    recipient = payload[0]
    sender = payload[1]
    incoming_msg_id = payload[2]
    incoming_length = payload[3]
    incoming = str(bytes(payload[4:]), 'utf-8')

    if incoming_length != len(incoming):
        print("Error: Message length mismatch!")
        return

    if recipient != local_address and recipient != 0xFF:
        print("This message is not for me.")
        return

    print("Received from device: 0x{:02X}".format(sender))
    print("Sent to: 0x{:02X}".format(recipient))
    print("Message ID: {}".format(incoming_msg_id))
    print("Message length: {}".format(incoming_length))
    print("Message: {}".format(incoming))
    print()

# Main function
def main():
    print("LoRa Communication - Ping & Pong")

    GPIO.output(reset_pin, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(reset_pin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(reset_pin, GPIO.HIGH)
    time.sleep(0.1)

    while True:
        last_send_time = 0
        if time.time() - last_send_time > interval:
            message = "Hi Supernova! :O"
            send_message(message)
            print("Sending:", message)
            last_send_time = time.time()

        if GPIO.input(irq_pin) == GPIO.LOW:
            payload = spi.readbytes(256)  # Adjust buffer size as needed
            on_receive(payload)
        sleep(2)

if True:
    last_send_time = 0
    main() 