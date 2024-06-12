import socket
import argparse

def tcp_client(server_host, server_port, payload_size):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_host, server_port))
            print(f"Connected to TCP server at {server_host}:{server_port}")
            
            payload = b'a' * payload_size
            client_socket.sendall(payload)
            print(f"Sent {payload_size} bytes")

            data = client_socket.recv(65536)
            print(f"Received {len(data)} bytes")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Client")
    parser.add_argument('--server_host', default='127.0.0.1', help='Server host')
    parser.add_argument('--server_port', type=int, default=12345, help='Server port')
    parser.add_argument('--payload_size', type=int, default=1024, help='Payload size in bytes')
    args = parser.parse_args()

    tcp_client(args.server_host, args.server_port, args.payload_size)
