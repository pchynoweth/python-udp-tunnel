import argparse
import numpy
import selectors
import socket

sel = selectors.DefaultSelector()

# Configuration
LISTEN_ADDRESS = '0.0.0.0'  # Listen on all available network interfaces
HOST_ADDRESS = '127.0.0.1'
HOST_PORT = 51821
DOCKER_ADDRESS = '172.17.0.2'
DOCKER_PORT = 51820

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
        print(f'Sent packet to {addr}:{port}')
    queue.clear()

def queueing(data):
    if data is None:
        return
    print('Queueing packet')
    queue.append(data)

def main():
    parser = argparse.ArgumentParser(
                    prog='tunnel.py',
                    description='UDP tunnel for testing')

    parser.add_argument('-l', '--listen-address', default=LISTEN_ADDRESS, help='Listen address')
    parser.add_argument('-p', '--listen-port', default=DOCKER_PORT, help='Listen port')
    parser.add_argument('-t', '--target-address', default=None, help='Target address')
    #parser.add_argument('-o', '--target-port', default=TARGET_PORT, help='Target port')

    parser.add_argument('-d', '--dropping-probability', type=int, default=0.1, help='Probability of dropping a packet')
    parser.add_argument('-q', '--queueing-probability', type=int, default=0.1, help='Probability of queueing a packet')

    args = parser.parse_args()

    forwarding_probability = 1 - args.dropping_probability - args.queueing_probability

    print(f"Forwarding probability: {forwarding_probability}")

    # Create a UDP socket for listening
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listen_socket.bind((LISTEN_ADDRESS, DOCKER_PORT))
    sel.register(listen_socket, selectors.EVENT_READ)

    print(f"Listening on {LISTEN_ADDRESS}:{DOCKER_PORT}")
    
    modes = [ dropping, forwarding, queueing ]
    probabilities = [ args.dropping_probability, forwarding_probability, args.queueing_probability ]
    while True:
        events = sel.select(timeout=0.1)
        mode = numpy.random.choice(modes, p=probabilities)
        mode(None)
        for key, _ in events:
            sock = key.fileobj
            data, addr = sock.recvfrom(1024)
            print(f"Received data from {addr}: {data}")
            address, port = addr
            if port == DOCKER_PORT:
                port = HOST_PORT
                address = HOST_ADDRESS
            else:
                port = DOCKER_PORT
                address = DOCKER_ADDRESS
            mode((listen_socket, address, port, data))
    
if __name__ == '__main__':
    main()