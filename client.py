import socket
import threading
import sys

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SPACE = "\n" * 50

class Client:
    def __init__(self, host, port):
        self.addr = (host, port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.addr)

    def receive_messages(self):
        while True:
            try:
                msg_length_data = self.client.recv(HEADER).decode(FORMAT)
                if not msg_length_data:
                    print("\n[ERROR] Connection lost with the server")
                    self.client.close()
                    break
                    
                msg_length = int(msg_length_data)
                msg = self.client.recv(msg_length).decode(FORMAT)
                print(f"\n{msg}\n> ", end="")
            except:
                print("\n[ERROR] Connection lost with the server")
                self.client.close()
                break

    def send_message(self):
        connected = True
        try:
            print(f'[CONNECTED] Connected to the server on {self.addr}. ')
            name = input('Type your name before entering the chat: ')
            print(SPACE)

            name_send = name.encode(FORMAT)
            name_length = str(len(name_send)).encode(FORMAT)
            name_length += b' ' * (HEADER - len(name_length))
            self.client.send(name_length)
            self.client.send(name_send)

            thread = threading.Thread(target=self.receive_messages, daemon=True)
            thread.start()

            while connected:
                msg = input("> ")
                message = msg.encode(FORMAT)
                msg_length = str(len(message)).encode(FORMAT)
                msg_length += b' ' * (HEADER - len(msg_length))
                self.client.send(msg_length)
                self.client.send(message)

                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    self.client.close()
                    break

        except Exception:
            print("[LOST CONNECTION] The server is down or the connection was lost")
        finally:
            print(f"{SPACE}+[CHAT ENDED]")
            sys.exit()

if __name__ == "__main__":
    # TYPE THE SERVER IP ADDRESS HERE TO CONNECT (for example "192.168.0.66" or "127.0.0.1")
    HOST = "192.168.0.79"
    
    # TYPE THE SERVER PORT HERE TO CONNECT (for example 5050)
    PORT = 5050

    client = Client(HOST, PORT)
    client.send_message()