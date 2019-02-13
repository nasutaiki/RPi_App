# coding: UTF-8
import certification, socket, time


if __name__ == '__main__':
    user_status = []                                   # 入退出の状態の管理を行うための配列
    myStruct = {'ID': '0000000000000000', 'Weight': 0} # 初期値
    user_status.append(myStruct)                       # 初期化

    # サーバに接続
    host = '192.168.43.7' # サーバーのホスト名
    port = 9999 # PORTを指定

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # オブジェクトの作成をします
    client.connect((host, port)) # サーバーに接続
    print('success connecting!')

    while True:
        # ID認証を行う
        user = certification.cardAuthentication()
        
        # 戻り値のユーザデータが空だったらID認証を再度行う
        if len(user) == 0:       
            print('sound control')
            client.send('n') # NGのサウンドを再生
            client.recv(4096)
            continue

        print('sound control')
        client.send('s') # OKのサウンドを再生
        client.recv(4096)

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

            # 管理者へ通知
            certification.sendLINE()
            
            print('sound control')
            client.send('n')
            client.recv(4096)

            continue
        
        certification.faceMatch(user['Image'], 85)
        
        print('sound control')
        client.send('s')
        client.recv(4096)

        # 顔認証成功時の処理
        if flg:
            certification.logRegistration(user, True, 'IN')
            
            # 重量センサーから値を取得
            print('weight control')
            client.send('o')
            weight = client.recv(4096)

            # 登録するユーザのデータを作成
            myStruct = {'ID': user['ID'], 'Weight': weight}
            
            # 入室したユーザのデータを追加
            user_status.append(myStruct)

        else:
            certification.logRegistration(user, True, 'OUT')
            
            print('weight control')
            client.send('i')
            weight = client.recv(4096)
            
            # 入室時と比べて退出時のほうが重量が大きければ退出させない
            if weight > user_status[place]['Weight']:
                certification.sendLINE()

                print('sound control')
                client.send('n')
                client.recv(4096)

                continue
            
            # 退出したユーザのデータを削除
            user_status.remove(user_status[place])
        
        # ステッピングモータの制御（開ける）
        print('motor control')
        client.send('f')
        client.recv(4096)

	time.sleep(3)
        
        # ステッピングモータの制御（閉める）
        print('motor control')
        client.send('b')
        client.recv(4096)

    client.close()
