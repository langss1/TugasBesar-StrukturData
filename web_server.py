import socket
import threading
import os

# Fungsi untuk handle request dari klien dalam thread
def handle_client(connection, address):
    try:
        print(f"[INFO] Connected by {address}")
        request = connection.recv(1024).decode()
        print(f"[REQUEST] {request}")

        if not request:
            connection.close()
            return

        # Ambil nama file dari request GET
        headers = request.split()
        if len(headers) < 2:
            connection.close()
            return

        filename = headers[1].lstrip('/')
        if filename == "":
            filename = "index.html"

        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                response_data = f.read()
            response_header = "HTTP/1.1 200 OK\r\n"
            response_header += f"Content-Length: {len(response_data)}\r\n"
            response_header += "Content-Type: text/html\r\n"
            response_header += "Connection: close\r\n\r\n"
            connection.sendall(response_header.encode() + response_data)
        else:
            response_body = "<html><body><h1>404 Not Found</h1></body></html>".encode()
            response_header = "HTTP/1.1 404 Not Found\r\n"
            response_header += f"Content-Length: {len(response_body)}\r\n"
            response_header += "Content-Type: text/html\r\n"
            response_header += "Connection: close\r\n\r\n"
            connection.sendall(response_header.encode() + response_body)
    finally:
        connection.close()
        print(f"[INFO] Connection closed for {address}")

# Main server function
def start_server(host='0.0.0.0', port=6789):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[START] Server listening on {host}:{port}")

    while True:
        client_conn, client_addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_conn, client_addr))
        thread.start()

if __name__ == "__main__":
    start_server()
