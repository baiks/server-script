import socket
import datetime
import threading


def handler(conn, addr):
    with conn:
        print(f"Connected from {addr}")
        while True:
            data = conn.recv(1024)
            print('Data : ', data)
            if not data:
                break
            text = data.decode('iso-8859-1')
            clean_text = text.strip()
            print('Requesting IP: ', str(addr))
            print('Search query: ', clean_text)
            print('Request Time: ', datetime.datetime.now())
            file = open('dummy.txt', 'r')
            content = file.read()
            file.close()
            print(content)
            if clean_text in content:
                conn.send('STRING EXISTS\n'.encode())
            else:
                conn.send('STRING NOT FOUND\n'.encode())
                print('Response Time: ', datetime.datetime.now())
        print(f'Disconnected from {addr}')


def intiateServer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 4444))
        print('Server Socket started: ', s)
        s.listen()

        while True:
            conn, addr = s.accept()
            print('Connecting from: ', str(addr[0]))
            threading.Thread(target=handler, args=(conn, addr)).start()
