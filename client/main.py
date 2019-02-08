# coding: UTF-8
import certification, time, socket


# TCP通信のコネクションを行う（クライアント）
class tcpClient():

    def init(self):
        host = '127.0.0.1' # サーバーのホスト名
        port = 12345 # PORTを指定

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # オブジェクトの作成をします
        self.client.connect((host, port)) # サーバーに接続
        print('success connecting!')

    # レスポンスを受け取る
    def tcpRecv(self):
        rcvmsg = self.client.recv(4096)
        return rcvmsg

    # データの送信
    def tcpSend(self, s_msg):
        self.client.send(s_msg)

    # 閉じる
    def tcpFinish(self):
        self.client.close()


if __name__ == '__main__':
    user_status = []                                   # 入退出の状態の管理を行うための配列
    myStruct = {'ID': '0000000000000000', 'Weight': 0} # 初期値
    user_status.append(myStruct)                       # 初期化

    # サーバに接続
    server = tcpClient()

    while True:
        # ID認証を行う
        user = certification.cardAuthentication()
        
        # 戻り値のユーザデータが空だったらID認証を再度行う
        if len(user) == 0:        
            server.tcpSend('n') # NGのサウンドを再生
            continue

        server.tcpSend('s') # OKのサウンドを再生
        time.sleep(2)

        flg = True    # trueなら入室、falseなら退出
        place = 0     # 現在認証中のユーザの位置を記憶
        # 入退出の判定
        for status in user_status:
            if user['ID'] == status['ID']:
                flg = False
                break
            
            place += 1

        # 顔認証を行う
        result = certification.faceAuthentication(user['Image'])
        
        # 顔認証失敗時の処理
        if not result:
            certification.faceMatch(user['Image'], 0)

            # 認証失敗時のLogを登録する　
            if flg:
                certification.logRegistration(user, False, 'IN')

            else:
                certification.logRegistration(user, False, 'OUT')
            
            server.tcpSend('n')
            continue
        
        certification.faceMatch(user['Image'], 85)
        
        # 顔認証成功時の処理
        if flg:
            certification.logRegistration(user, True, 'IN')
            
            # 重量センサーから値を取得
            server.tcpSend('o')
            weight = server.tcpRecv()

            # 登録するユーザのデータを作成
            myStruct = {'ID': user['ID'], 'Weight': weight}
            
            # 入室したユーザのデータを追加
            user_status.append(myStruct)

        else:
            certification.logRegistration(user, True, 'OUT')

            server.tcpSend('i')
            weight = server.tcpRecv()
            
            # 入室時と比べて退出時のほうが重量が大きければ退出させない
            if weight > user_status[place]['Weight']:
                server.tcpSend('n')
                continue
            
            # 退出したユーザのデータを削除
            user_status.remove(user_status[place])
        
        server.tcpSend('s')
        time.sleep(2)

        # DCモータの制御（開ける）
        server.tcpSend('f')
        time.sleep(3)
        
        # DCモータの制御（開ける）
        server.tcpSend('b')
        time.sleep(1)

    server.tcpFinish()