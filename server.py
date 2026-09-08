import socket
import threading

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

class Server:
    def __init__(self, host, port):
        self.addr = (host, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.addr)
        self.clients = []

    def handle_client(self, conn, addr):
        print(f'[NEW CONNECTION] {addr} connected.')
        connected = True

        name_length_data = conn.recv(HEADER).decode(FORMAT)
        if not name_length_data:
            conn.close()
            return
            
        name_length = int(name_length_data)
        name = conn.recv(name_length).decode(FORMAT)

        try:
            while connected:
                msg_length_data = conn.recv(HEADER).decode(FORMAT)
                if not msg_length_data:
                    break
                    
                msg_length = int(msg_length_data)
                msg = conn.recv(msg_length).decode(FORMAT)

                self.broadcast(msg, conn, name)
                print(f'{name}: {msg}')

                if msg == DISCONNECT_MESSAGE:
                    connected = False

        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            print(f"[DISCONNECTED] {name} disconnected.")

        finally:
            if conn in self.clients:
                self.clients.remove(conn)
            conn.close()

    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.addr}")
        while True:
            conn, addr = self.server.accept()
            self.clients.append(conn)
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    def broadcast(self, msg, sender_conn, name):
        for client in self.clients.copy():
            if client != sender_conn:
                try:
                    full_msg = f"[{name}]: {msg}"
                    msg_encoded = full_msg.encode(FORMAT)
                    msg_length = str(len(msg_encoded)).encode(FORMAT)
                    msg_length += b' ' * (HEADER - len(msg_length))

                    client.send(msg_length)
                    client.send(msg_encoded)
                except:
                    if client in self.clients:
                        self.clients.remove(client)

if __name__ == "__main__":
    # TYPE YOUR SERVER IP ADDRESS HERE (for example "192.168.0.66", "127.0.0.1" for localhost, or "0.0.0.0")
    HOST = "192.168.0.79"
    
    # TYPE YOUR SERVER PORT HERE (for example 5050)
    PORT = 5050

    server = Server(HOST, PORT)
    print("[STARTING] Server is starting...")
    server.start()