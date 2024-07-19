import sys
import socket
import threading
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtGui import QKeyEvent
import keyboard  # Убедитесь, что у вас установлен модуль keyboard: pip install keyboard

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"JavaScript Console Message: {message} (Level: {level}, Line: {lineNumber}, Source: {sourceID})")
        if "Scripts may close only the windows that were opened by them." in message:
            self.view.load(QUrl.fromLocalFile("/Users/mafan2010/Scour-TV_OS-0.1/venv/UI/index.html"))

class FullscreenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UI")
        self.setGeometry(100, 100, 800, 600)
        self.webview = QWebEngineView(self)
        self.setCentralWidget(self.webview)
        self.showFullScreen()

        self.page = CustomWebEnginePage(self.webview)
        self.webview.setPage(self.page)
        self.page.view = self.webview

        profile = self.webview.page().profile()
        custom_user_agent = "Mozilla/5.0 (SMART-TV; Linux; Tizen 4.0.0.2) AppleWebkit/605.1.15 (KHTML, like Gecko) SamsungBrowser/9.2 TV Safari/605.1.15"
        profile.setHttpUserAgent(custom_user_agent)

        self.webview.load(QUrl.fromLocalFile("/Users/mafan2010/Scour-TV_OS-0.1/venv/UI/index.html"))

        # Запускаем сервер
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.daemon = True
        self.server_thread.start()

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('192.168.1.63', 65432))  # Укажите ваш IP-адрес и порт
        server_socket.listen(1)

        print("Server listening on 192.168.1.63:65432")

        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")

        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            self.handle_command(data)

        conn.close()

    def handle_command(self, command):
        print(f"Received command: {command}")
        if command == "ArrowUp":
            keyboard.send("up")
        elif command == "ArrowDown":
            keyboard.send("down")
        elif command == "ArrowLeft":
            keyboard.send("left")
        elif command == "ArrowRight":
            keyboard.send("right")
        elif command == "Back":
            keyboard.send("esc")
        elif command == "Ok":
            keyboard.send("enter")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FullscreenWindow()
    window.show()
    sys.exit(app.exec_())
