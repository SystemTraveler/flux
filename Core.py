import sys
import threading
import re
import pygame
import speech_recognition as sr
from gtts import gTTS
from g4f.client import Client
import asyncio
import websockets
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
import keyboard
import socket

pygame.mixer.init()

# Загрузка звукового файла
sound = pygame.mixer.Sound('UI/media/connect.wav')
ai_sound = pygame.mixer.Sound('UI/media/ai.mp3')

# Инициализация клиента и текстового-во-голосового движка
client = Client()

def clean_text(text):
    """Очистить текст от нежелательных символов."""
    return re.sub(r'[^\w\s]', '', text)

def text_to_speech(text, lang='ru'):
    """Конвертировать текст в речь и воспроизвести его."""
    tts = gTTS(text=text, lang=lang)
    tts.save("response.mp3")
    pygame.mixer.music.load("response.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def recognize_speech_from_mic(lang='ru-RU'):
    """Распознавание речи с микрофона."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Скажите что-нибудь...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language=lang)
            print(f"Вы сказали: {text}")
            return extract_volume_from_text(clean_text(text))
        except sr.UnknownValueError:
            print("Не удалось распознать аудио")
            return None
        except sr.RequestError as e:
            print(f"Ошибка сервиса распознавания: {e}")
            return None

def extract_volume_from_text(text):
    """Извлечь громкость из текста."""
    match = re.search(r'\b(\d+)\b', text)
    if match:
        return int(match.group(1))
    return None

def get_response_from_gpt(message):
    """Получить ответ от GPT-3.5."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message + ". Ответь на русском языке!!!!!"}]
    )
    return response.choices[0].message.content

def get_local_ip():
    """Получить IP-адрес текущего компьютера, который не является localhost."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except Exception as e:
        print(f"Ошибка при получении IP-адреса: {e}")
        local_ip = None
    finally:
        s.close()
    return local_ip

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index_url = QUrl.fromLocalFile("/Users/mafan2010/Scour-TV_OS-0.1/venv/UI/index.html")

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"JavaScript Console Message: {message} (Level: {level}, Line: {lineNumber}, Source: {sourceID})")
        if message.startswith("Scripts may close only the windows that were opened by them"):
            self.view.setUrl(self.index_url)

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

        self.home_url = QUrl.fromLocalFile("/Users/mafan2010/Scour-TV_OS-0.1/venv/UI/index.html")
        self.webview.load(self.home_url)

        local_ip = get_local_ip()
        if local_ip:
            print(f"Server will listen on IP: {local_ip}, Port: 65432")

        # Воспроизвести звук подключения
        sound.play()

        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.daemon = True
        self.server_thread.start()

        self.voice_active = False
        self.voice_thread = None
        self.voice_stop_event = threading.Event()
        self.voice_stop_event.set()

    async def handle_client(self, websocket, path):
        print(f"Client connected: {websocket.remote_address}")
        try:
            while True:
                data = await websocket.recv()
                if data:
                    print(f"Received command: {data}")
                    self.handle_command(data)
                    await websocket.send(f"Received: {data}")
                else:
                    break
        except websockets.ConnectionClosed:
            print(f"Connection with {websocket.remote_address} closed")

    def start_server(self):
        async def main():
            server = await websockets.serve(self.handle_client, '0.0.0.0', 65432)
            print(f"WebSocket server listening on ws://0.0.0.0:65432")
            await server.wait_closed()

        asyncio.run(main())

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
        elif command == "AI":
            ai_sound.play()
            self.stop_voice_command()
            self.start_voice_command()

    def set_volume_from_command(self, command):
        volume = extract_volume_from_text(command)
        if volume is not None and 0 <= volume <= 100:
            pygame.mixer.music.set_volume(volume / 100.0)
            print(f"Volume set to {volume}%")
            text_to_speech(f"Громкость установлена на {volume} процентов")
        else:
            print("Не удалось установить громкость. Укажите значение от 0 до 100.")

    def navigate_to_home(self):
        self.webview.setUrl(self.home_url)

    def start_voice_command(self):
        self.voice_active = True
        self.voice_stop_event.clear()
        ai_sound.play()
        self.voice_thread = threading.Thread(target=self.listen_for_voice_command)
        self.voice_thread.daemon = True
        self.voice_thread.start()

    def stop_voice_command(self):
        self.voice_active = False
        self.voice_stop_event.set()
        if self.voice_thread:
            self.voice_thread.join()
        pygame.mixer.music.stop()

    def listen_for_voice_command(self):
        while not self.voice_stop_event.is_set():
            user_message = recognize_speech_from_mic()
            if user_message:
                gpt_response = get_response_from_gpt(user_message)
                print(f"Ответ GPT: {gpt_response}")
                text_to_speech(gpt_response)
                ai_sound.play()
            else:
                self.stop_voice_command()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FullscreenWindow()
    window.show()
    sys.exit(app.exec_())
