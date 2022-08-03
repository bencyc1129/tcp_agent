import socket
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", nargs= '?', type= str, default= '127.0.0.1')
    parser.add_argument("-p", nargs= '?', type= int, default= 7000)

    args = parser.parse_args()
    hostIP = args.i
    port = args.p

    print(hostIP, port)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((hostIP, port))
    s.listen(5)
    print(f'Listening at: {hostIP}:{port}')
    listening = True

    while listening:
        conn, addr = s.accept()
        print(f'Connected by: {addr[0]}:{addr[1]}')

        while True:
            command = input('Please input command: ')
            if command == "": continue

            conn.send(command.encode())

            if command == 'exit': 
                print('Session break!')
                listening = False
                break
            
            buffer = ''
            while True:
                indata = conn.recv(4096).decode()
                buffer += indata

                if 'END' in indata: 
                    print(buffer[:-3])
                    break

    s.close()


if __name__ == '__main__':
    main()