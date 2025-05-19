import tkinter as tk
from socket import *
from PIL import Image, ImageTk

target_ip = "172.21.12.27"
port = 5001

# Defing the request from client to server
def send_crossing_request(target_ip):
    try:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect((target_ip, port))
            sock.send(b'pedestrian_crossing')
            response = sock.recv(1024).decode()
            response_label.config(text="Server reply: " + response)
    except Exception as e:
        response_label.config(text="Connection error: " + str(e))


# Unique GUI component for pedestrian interaction
def start_client():
    window = tk.Tk()
    window.title("Pedestrian Crossing")
    window.geometry("450x350")
    window.configure(bg="#ffffff")

    # Load and resize the image
    img = Image.open("click_to_cross.png")  # Use the downloaded/redesigned file
    img = img.resize((200, 200), Image.Resampling.LANCZOS)
    button_img = ImageTk.PhotoImage(img)

    # Image button
    image_button = tk.Button(window, image=button_img, command=lambda: send_crossing_request(target_ip), borderwidth=0, bg="#ffffff", activebackground="#ffffff")
    image_button.image = button_img  # Keep a reference
    image_button.pack(pady=20)

    global response_label
    response_label = tk.Label(window, text="", font=("Helvetica", 12), bg="#ffffff")
    response_label.pack(pady=10)

    window.mainloop()

start_client()

