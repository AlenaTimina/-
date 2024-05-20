from socket import *

host = "127.0.0.1"
port = 8000
filename = "1.html"

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

client_socket.connect((host, port))
client_socket.sendall(f"GET /{filename} HTTP/1.1\r\nHost: {host}\r\n\r\n".encode())

result = b""
while True:
    data = client_socket.recv(1024)
    if not data:
        break
    result += data

res = result.decode("utf-8")
print(res)
client_socket.close()
