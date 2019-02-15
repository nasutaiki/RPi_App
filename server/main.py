# coding: UTF-8
import socket, control


if __name__ == '__main__':
    # TCP通信のセットアップ
    host = '192.168.43.7' # サーバーのホスト名
    port = 9999 # PORTを指定

    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversock.bind((host,port)) # IPとPORTを指定してバインド
    serversock.listen(10) # 接続の待ち受け（キューの最大数を指定）
    print('コネクション待ち...')

    clientsock, client_address = serversock.accept() # 接続されればデータを格納
    print('コネクションに成功しました！')

    while True:
        mode = clientsock.recv(1024)

        if mode == b'f': # 扉を開ける
            control.stepControl('f')
            clientsock.sendall(0) #メッセージを返す

        elif mode == b'b': # 扉を閉める
            control.stepControl('b')
            clientsock.sendall(0)

        elif mode == b'o': # 入室時
            weight = control.getWeight('o')
            clientsock.sendall(weight)

        elif mode == b'i': # 退出時
            weight = control.getWeight('i')
            clientsock.sendall(weight)

        elif mode == b's': # 認証成功
            control.soundControl('shonin.mp3')

        elif mode == b'n': # 認証失敗
            control.soundControl('keikoku.mp3')
    
    clientsock.close()
