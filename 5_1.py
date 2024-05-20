from socket import *
import os
import time

# Создаем сокет для сервера
hostname = "127.0.0.1"
port = 8000
# параметры отвечают за IPv4 и TCP
serverSocket = socket(AF_INET, SOCK_STREAM)
# использовать один и тот же локальный адрес и порт,
# если они ранее использовались, но еще находятся в состоянии "TIME_WAIT"
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Связаваем сокет с хостом и протоколом
serverSocket.bind((hostname, port))

# переводим в режим прослушивания
# 1 - максимальное кол-во подключений, которые могут находиться в очереди на установление соединения
serverSocket.listen(1)
print(f"http://{hostname}:{port}/1.html")


while True:
    try:
        # Получаем новый сокет и адресс клиента
        connectionSocket, addr = serverSocket.accept()
        print("Подключение успешно установлено")
        request = connectionSocket.recv(1024).decode()
        print("Запрос:", request.split("\n")[0])
        print()
        time.sleep(5)

        filename = request.split()[1][1:]

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
            answer = (
                f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{content}".encode()
            )
            print("Ответ: ", answer)
        else:
            answer = b"HTTP/1.1 404 Not Found\r\n\r\n404 Not Found"
            print("Ответ: ", answer)
            print()
            print()

        connectionSocket.sendall(answer)
        connectionSocket.close()

    except IOError:
        connectionSocket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n404 Not Found")

        connectionSocket.close()

        serverSocket.close()
