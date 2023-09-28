import socket

HOSTNAME = socket.gethostname()
IP = socket.gethostbyname_ex(HOSTNAME)[2][1]

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, 3000))

    # start listening and print
    while True:
        try:
            print('vamo ve se agr vai')
            msg = 'enviando msg'
            sock.sendto(msg.encode('utf-8'), (socket.gethostbyname_ex(HOSTNAME)[2][1], 3001))
        except:
            print('vsff')
            pass

