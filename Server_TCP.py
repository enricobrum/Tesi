import socket
import argparse

def start_tcp_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"TCP server listening on {host}:{port}")
        
        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(65536)
                    if not data:
                        break
                    print(f"Received {len(data)} bytes from {addr}")
                    conn.sendall(data)  # Echo back the data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Server")
    parser.add_argument('--host', default='0.0.0.0', help='Host to listen on')
    parser.add_argument('--port', type=int, default=12345, help='Port to listen on')
    args = parser.parse_args()

    start_tcp_server(args.host, args.port)
