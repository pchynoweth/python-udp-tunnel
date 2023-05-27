import socket

# Configuration
LISTEN_ADDRESS = '0.0.0.0'  # Listen on all available network interfaces
LISTEN_PORT = 54321  # Port to listen on

def main():
    # Create a UDP socket for listening
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listen_socket.bind((LISTEN_ADDRESS, LISTEN_PORT))
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while True:
        # Receive data from the client
        data, addr = listen_socket.recvfrom(1024)
        print(f"Received data from {addr}: {data.decode()}")
        
        # Create a UDP socket for sending to the target server
        listen_socket.sendto(data, addr)
    
if __name__ == '__main__':
    main()