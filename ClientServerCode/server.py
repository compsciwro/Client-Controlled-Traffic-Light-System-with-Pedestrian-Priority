from gpiozero import TrafficLights
from time import sleep
from socket import *
import _thread

 #Define the GPIO pins for the traffic lights
PIN_RED = 17
PIN_GREEN = 22
PIN_AMBER = 27

TrafficSignal = TrafficLights(PIN_RED, PIN_GREEN, PIN_AMBER)

#Global flags for the pedestrian request 
pedestrian_waiting = False
client_socker = None

#Connecting client and server code
global client_requested,connection_socket
client_requested = False
connection_socket = None

# Handling the request
def handle_requests():
    global pedestrian_waiting, client_socket
 
    host_ip = "172.21.12.27"
    host_port = 5001

    server = socket(AF_INET, SOCK_STREAM)
    server.bind((host_ip, host_port))
    server.listen(1)

    print("Traffic Light Server active and listening...") #prints on client side

    while True:
        client_socket, client_address = server.accept()
        print("Pedestrian crossing request received.") # prints on client side
        message = client_socket.recv(1024).decode()
        if message.strip() == "pedestrian_crossing":
            pedestrian_waiting = True

# Start thread for incoming pedestrian requests
_thread.start_new_thread(handle_requests, ())

def manage_traffic():
    global pedestrian_waiting, client_socket
    while True:
        # Green signal for vehicles
        TrafficSignal.green.on()
        sleep(4)
        TrafficSignal.green.off()

        if pedestrian_waiting:
            # Switch to amber, then red for pedestrian crossing
            TrafficSignal.amber.on()
            sleep(2)
            TrafficSignal.amber.off()

            TrafficSignal.red.on()
            if client_socket:
                client_socket.send(b"Pedestrian may now cross safely.") #prints on GUI 
            sleep(5)
            TrafficSignal.red.off()

            pedestrian_waiting = False  # Reset request state
        else:
            # Normal traffic cycle with amber and red lights
            TrafficSignal.amber.on()
            sleep(2)
            TrafficSignal.amber.off()

            TrafficSignal.red.on()
            sleep(3)
            TrafficSignal.red.off()

def start_control_system():
    manage_traffic()

# Start the traffic control system
start_control_system()
