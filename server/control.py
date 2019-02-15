# coding: UTF-8
import time, serial


# Arduinoと接続
print('connecting Arduino')
Arduino = serial.Serial('/dev/ttyUSB0', 9600)
print('success!')

# ArduinoとSerial通信を行う
def serialControl(req):
    # 命令を送る
    Arduino.write(req)
    time.sleep(1)
    
    # レスポンスを受け取る
    line = '1023'
    line = Arduino.readline()
    time.sleep(1)
    
    return int(line)


# 扉の開閉を行うステッピングモータの制御
def stepControl(req):
    print('ステッピングモータ制御中...')
    serialControl(req)
    print('Finish.')


# ユーザの重量を取得する関数
def getWeight(req):
    print('重量チェック中...')
    weight = serialControl(req)
    print('Finish.')
    return weight


# 認証の結果に応じて出力する音の制御
def soundControl(sound):
    pygame.mixer.init()

    # 音楽ファイルの読み込み
    pygame.mixer.music.load(sound)

    # 音楽再生、および再生回数の設定
    pygame.mixer.music.play(1)
    time.sleep(60)

    # 再生の終了
    pygame.mixer.music.stop()
    print('Finish.')