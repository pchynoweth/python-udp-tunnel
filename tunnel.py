import socket
import selectors
import numpy

sel = selectors.DefaultSelector()

# Configuration
LISTEN_ADDRESS = '0.0.0.0'  # Listen on all available network interfaces
LISTEN_PORT = 12345  # Port to listen on
LISTEN_PORT2 = 12346
TARGET_ADDRESS = '127.0.0.1'  # IP address of the target server
TARGET_PORT = 56789  # Port of the target server
TARGET_PORT2 = 54321

queue = list()

def dropping(data):
    if data is None:
        return
    print('Dropping packet')

def forwarding(data):
    if data:
        queue.append(data)
    for d in queue:
        sock, addr, port, send_data = d
        sock.sendto(send_data, (addr, port))
    if queue:
        print('Sent packet')
    queue.clear()

def queueing(data):
    if data is None:
        return
    print('Queueing packet')
    queue.append(data)

def main():
    # Create a UDP socket for listening
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listen_socket.bind((LISTEN_ADDRESS, LISTEN_PORT))
    listen_socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listen_socket2.bind((LISTEN_ADDRESS, LISTEN_PORT2))
    sel.register(listen_socket, selectors.EVENT_READ, data=(listen_socket2, TARGET_ADDRESS, TARGET_PORT2))
    sel.register(listen_socket2, selectors.EVENT_READ, data=(listen_socket, TARGET_ADDRESS, TARGET_PORT))

    print(f"Listening on {LISTEN_ADDRESS}:{LISTEN_PORT} and republishing to {TARGET_ADDRESS}:{TARGET_PORT}")
    
    modes = [ dropping, forwarding, queueing ]
    mode = numpy.random.choice(modes, p=[0.1, 0.8, 0.1])
    while True:
        events = sel.select(timeout=0.1)
        mode = numpy.random.choice(modes, p=[0.1, 0.8, 0.1])
        mode(None)
        for key, _ in events:
            sock = key.fileobj
            data, addr = sock.recvfrom(1024)
            print(f"Received data from {addr}: {data.decode()}")
            sock, addr, port = key.data
            mode((sock, addr, port, data))
    
if __name__ == '__main__':
    main()