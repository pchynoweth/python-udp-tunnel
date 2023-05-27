import socket

# Configuration
LISTEN_ADDRESS = '0.0.0.0'  # Listen on all available network interfaces
LISTEN_PORT = 56789  # Port to listen on
TARGET_ADDRESS = '127.0.0.1'  # IP address of the target server
TARGET_PORT = 12345

def main():
    # Create a UDP socket for listening
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listen_socket.bind((LISTEN_ADDRESS, LISTEN_PORT))

    # Create a UDP socket for sending to the target server
    listen_socket.sendto(str.encode("Hello"), (TARGET_ADDRESS, TARGET_PORT))

    # Receive data from the client
    data, addr = listen_socket.recvfrom(1024)
    print(f"Received data from {addr}: {data.decode()}")
    
if __name__ == '__main__':
    main()