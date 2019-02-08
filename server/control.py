# coding: UTF-8
import time, serial


# ArduinoとSerial通信を行う
def serialControl(device, req):
    # 初期化
    arduino = serial.Serial('/dev/ttyUSB0', 9600)
    time.sleep(2)

    # 命令を送る
    arduino.write(req)
    time.sleep(1)
    
    # レスポンスを受け取る
    line = '1023'
    line = arduino.readline()
    time.sleep(1)
    
    arduino.close()
    return int(line)


# 扉の開閉を行うDCモータの制御
def dcmControl(req):
    print('DCモータ制御中...')
    serialControl(devices['dc'], req)


# ユーザの重量を取得する関数
def getWeight():
    print('重量チェック中...')
    weight = serialControl(devices['weight'], 'g')
    return weight


# 認証の結果に応じて出力する音の制御
def soundControlOK():
    pygame.mixer.init()
    # 音楽ファイルの読み込み
    pygame.mixer.music.load('shonin.mp3')
    # 音楽再生、および再生回数の設定
    pygame.mixer.music.play(1)
    time.sleep(60)
    # 再生の終了
    pygame.mixer.music.stop()


def soundControlNG():
    pygame.mixer.init()
    # 音楽ファイルの読み込み
    pygame.mixer.music.load('keikoku.mp3')
    # 音楽再生、および再生回数の設定
    pygame.mixer.music.play(1)
    time.sleep(60)
    # 再生の終了
    pygame.mixer.music.stop()