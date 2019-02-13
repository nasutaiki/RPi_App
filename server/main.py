# coding: UTF-8
import socket, control


if __name__ == '__main__':
    # TCP通信のセットアップ
    host = '172.20.10.4' # サーバーのホスト名
    port = 12345 # PORTを指定

    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversock.bind((host,port)) # IPとPORTを指定してバインド
    serversock.listen(10) # 接続の待ち受け（キューの最大数を指定）
    print('コネクション待ち...')

    clientsock, client_address = serversock.accept() # 接続されればデータを格納
    print('コネクションに成功しました！')

    while True:
        mode = clientsock.recv(1024)
        if mode == 'f':
            control.stepControl('f')
            clientsock.sendall(0) #メッセージを返す
        elif mode == 'b':
            control.stepControl('b')
            clientsock.sendall(0)
        elif mode == 'o':
            weight = control.getWeight('o')
            clientsock.sendall(weight)
        elif mode == 'i':
            weight = control.getWeight('i')
            clientsock.sendall(weight)
        elif mode == 's':
            control.soundControlOK()
        elif mode == 'n':
            control.soundControlNG()
    
    clientsock.close()
