from threading import Thread
from socket import *
from time import sleep


def process_client(connectionSocket):
    try:
        request = connectionSocket.recv(1024).decode()
        filename = request.split()[1]

        with open(filename[1:], "r") as f:
            outputdata = f.read()

        header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        connectionSocket.send(header.encode())
        connectionSocket.send(outputdata.encode())
        print(outputdata)
        sleep(5)
        connectionSocket.close()

    except IOError:
        header = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
        answer = "<html><body>404 Not Found</body></html>"
        print(answer)
        connectionSocket.send(header.encode())
        connectionSocket.send(answer.encode())
        connectionSocket.close()


def start_server():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    hostname = "127.0.0.1"
    port = 8000
    serverSocket.bind((hostname, port))
    serverSocket.listen(1)
    print(f"http://{hostname}:{port}/1.html")
    try:
        while True:
            clientSocket, addr = serverSocket.accept()
            print()
            print(
                f"Соединение установленно из IP-адреса клиента и порта клиента {addr}"
            )
            print()
            client_thread = Thread(target=process_client, args=(clientSocket,))
            client_thread.start()

    except KeyboardInterrupt:
        serverSocket.close()


if __name__ == "__main__":
    start_server()
