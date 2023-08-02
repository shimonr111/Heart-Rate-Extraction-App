import socket
import sys
from PyQt5.QtWidgets import QApplication
from loginScreen import LoginScreen

def main():
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 5000
    ADDR = (IP, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

    # Create the application
    app = QApplication(sys.argv)
    window = LoginScreen(app, client)  # Pass the client socket to the LoginScreen
    window.show()
    app.exec()

    # Disconnect the client when the GUI is closed
    try:
        client.send('DISCONNECT'.encode("utf-8"))
    except socket.error as e:
        pass
    finally:
        client.close()

if __name__ == "__main__":
    main()
