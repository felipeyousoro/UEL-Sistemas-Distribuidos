import socket

HOSTNAME = socket.gethostname()
IP = socket.gethostbyname_ex(HOSTNAME)[2][0]

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, 3000))

    # start listening and print
    while True:
        try:
            msg = 'GAYYY'
            sock.sendto(msg.encode('utf-8'), ('26.63.64.96', 3001))
        except:
            print('vsff')
            pass

