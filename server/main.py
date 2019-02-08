# coding: UTF-8
import socket, control

class tcpServer():

    def init(self):
        # TCP通信のセットアップ
        host = '127.0.0.1' # サーバーのホスト名
        port = 12345 # PORTを指定
        
        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversock.bind((host,port)) # IPとPORTを指定してバインド
        serversock.listen(10) # 接続の待ち受け（キューの最大数を指定）
        print('コネクション待ち...')

        self.clientsock, client_address = serversock.accept() # 接続されればデータを格納
        print('コネクションに成功しました！')

    def tcpRecv(self):
        rcvmsg = self.clientsock.recv(1024)
        return rcvmsg

    def tcpSend(self, s_msg):
        self.clientsock.sendall(s_msg) #メッセージを返します

    def tcpFinish(self):
        self.clientsock.close()


if __name__ == '__main__':
    client = tcpServer()

    while True:
        mode = client.tcpRecv()
        if mode == 'f':
            control.dcmControl('f')
        elif mode == 'b':
            control.dcmControl('b')
        elif mode == 'o':
            weight = control.getWeight('o')
            client.tcpSend(weight)
        elif mode == 'i':
            weight = control.getWeight('i')
            client.tcpSend(weight)
        elif mode == 's':
            control.soundControlOK()
        elif mode == 'n':
            control.soundControlNG()
    
    client.tcpFinish()