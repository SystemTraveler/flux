import socket
import tkinter as tk

class RemoteControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Remote Control")
        
        # Create socket connection
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('192.168.1.63', 65432))  # Укажите IP-адрес и порт сервера
        
        # Create buttons
        self.create_buttons()

    def create_buttons(self):
        # Create a frame for arrow buttons
        arrow_frame = tk.Frame(self.root)
        arrow_frame.grid(row=0, column=1, rowspan=3, columnspan=3, padx=10, pady=10)

        # Arrow Up Button
        self.button_up = tk.Button(arrow_frame, text="↑", command=lambda: self.send_command("ArrowUp"), width=5, height=2)
        self.button_up.grid(row=0, column=1, padx=5, pady=5)

        # Arrow Down Button
        self.button_down = tk.Button(arrow_frame, text="↓", command=lambda: self.send_command("ArrowDown"), width=5, height=2)
        self.button_down.grid(row=2, column=1, padx=5, pady=5)

        # Arrow Left Button
        self.button_left = tk.Button(arrow_frame, text="←", command=lambda: self.send_command("ArrowLeft"), width=5, height=2)
        self.button_left.grid(row=1, column=0, padx=5, pady=5)

        # Arrow Right Button
        self.button_right = tk.Button(arrow_frame, text="→", command=lambda: self.send_command("ArrowRight"), width=5, height=2)
        self.button_right.grid(row=1, column=2, padx=5, pady=5)

        # OK Button inside arrow buttons
        self.button_ok = tk.Button(arrow_frame, text="OK", command=lambda: self.send_command("Ok"), width=5, height=2)
        self.button_ok.grid(row=1, column=1, padx=5, pady=5)

        # Back Button
        self.button_back = tk.Button(self.root, text="Back", command=lambda: self.send_command("Back"), width=10, height=2)
        self.button_back.grid(row=3, column=1, padx=10, pady=10)

        # Home Button (added to be right of Back Button)
        self.button_home = tk.Button(self.root, text="AI", command=lambda: self.send_command("AI"), width=10, height=2)
        self.button_home.grid(row=3, column=2, padx=10, pady=10)

    def send_command(self, command):
        try:
            print(f"Sending command: {command}")
            self.socket.sendall(command.encode())
        except Exception as e:
            print(f"Error sending command: {e}")

    def __del__(self):
        # Close the socket when the application is closed
        self.socket.close()

# Создаем корневое окно Tkinter и запускаем приложение
root = tk.Tk()
app = RemoteControlApp(root)
root.mainloop()
