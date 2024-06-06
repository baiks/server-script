import socket
import datetime
import threading
import configparser
import ssl

config = configparser.ConfigParser()
config.read('config.ini')


def handler(conn, addr, content):
    with conn:
        print(f"Connected from {addr}")
        while True:
            data = conn.recv(1024)
            print('Data : ', data)
            if not data:
                break
            text = data.decode('ISO-8859-1')
            clean_text = text.strip()
            print('Requesting IP: ', str(addr))
            print('Search query: ', clean_text)
            start_date = datetime.datetime.now()
            print('Request Time: ', datetime.datetime.now())
            if config.get('PATHS', 'REREAD_ON_QUERY') == 'False':
                print('Reading file on search query..')
                file = open(config.get('PATHS', 'linuxpath'), 'r')
                content = file.read().splitlines()
                file.close()
            if clean_text in content:
                conn.send('STRING EXISTS\n'.encode())
            else:
                conn.send('STRING NOT FOUND\n'.encode())
            end_date = datetime.datetime.now()
            print('Response Time: ', end_date)
            print('Execution time in seconds: ', (end_date - start_date).total_seconds())
        print(f'Disconnected from {addr}')


def intiateServer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((config.get('SOCKET', 'host'), int(config.get('SOCKET', 'port'))))
        print('Server Socket started: ', s)
        s.listen()
        content = []
        if config.get('PATHS', 'REREAD_ON_QUERY') == 'True':
            print('Reading file just once..')
            file = open(config.get('PATHS', 'linuxpath'), 'r')
            content = file.read().splitlines()
            file.close()

        while True:
            conn, addr = s.accept()
            ssl_socket = ssl.wrap_socket(conn, server_side=True, certfile='server.crt', keyfile='server.key',
                                         ssl_version=ssl.PROTOCOL_TLS)
            print('Connecting from: ', str(addr[0]))
            threading.Thread(target=handler, args=(ssl_socket, addr, content)).start()
