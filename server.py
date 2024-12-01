import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

# Function to connect to the server
def connect_to_server(nickname):
    server_host = '0.0.0.0'
    server_port = 55555
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((server_host, server_port))  # Connect to server
        client.send(nickname.encode('utf-8'))  # Send the nickname to the server
    except Exception as e:
        messagebox.showerror("Connection Error", f"Could not connect to server: {e}")
        return

    # GUI Setup for the chat window
    def setup_chat_window():
        root = tk.Tk()
        root.title(f"Chat - {nickname}")

        chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, state=tk.DISABLED)
        chat_area.pack(padx=10, pady=10)

        # Function to send messages
        def send_message():
            message = message_input.get()
            if message.strip():  # Send non-empty messages
                chat_area.config(state=tk.NORMAL)  # Enable text widget for inserting
                chat_area.insert(tk.END, f"You: {message}\n")
                chat_area.config(state=tk.DISABLED)  # Disable text widget again
                client.send(message.encode('utf-8'))
                message_input.delete(0, tk.END)

        # Function to receive messages
        def receive_message():
            while True:
                try:
                    message = client.recv(1024).decode('utf-8')
                    chat_area.config(state=tk.NORMAL)
                    chat_area.insert(tk.END, f"{message}\n")  # Show username + message
                    chat_area.config(state=tk.DISABLED)
                except:
                    messagebox.showerror("Connection Error", "Disconnected from server")
                    break

        message_input = tk.Entry(root, width=40)
        message_input.pack(padx=10, pady=5)

        send_button = tk.Button(root, text="Send", width=20, command=send_message)
        send_button.pack(pady=5)

        # Start the thread to receive messages
        receive_thread = threading.Thread(target=receive_message, daemon=True)
        receive_thread.start()

        root.mainloop()

    # After the nickname is entered, launch the chat window
    setup_chat_window()

# Nickname entry page
def nickname_page():
    def on_submit():
        nickname = nickname_input.get()
        if nickname.strip():  # Ensure the nickname is not empty
            nickname_window.destroy()
            connect_to_server(nickname)
        else:
            nickname_input.delete(0, tk.END)  # Clear the input if it's empty

    # Tkinter window for nickname input
    nickname_window = tk.Tk()
    nickname_window.title("Enter Nickname")

    label = tk.Label(nickname_window, text="Enter your nickname:")
    label.pack(padx=10, pady=10)

    nickname_input = tk.Entry(nickname_window, width=30)
    nickname_input.pack(padx=10, pady=10)

    submit_button = tk.Button(nickname_window, text="Submit", command=on_submit)
    submit_button.pack(pady=10)

    nickname_window.mainloop()

# Run the nickname page when the client starts
nickname_page()
