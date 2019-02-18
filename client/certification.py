# coding: UTF-8
import commands, requests, json, os, boto3, urllib2, random, serial, time


# Arduinoと接続
print('connecting Arduino')
Arduino = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2)
print('success!')

# Arduinoに信号を送ってLED制御をする
def ledControl(req):
    print('LED control')
    # 命令を送る
    Arduino.write(req)
    time.sleep(1)


# ID認証を行う関数
def cardAuthentication():
    print('ID認証中...')
    
    # NFCから情報を取得
    res = commands.getoutput('python ./nfc/tagtool.py')

    # IDを探す
    cardID = res.find('ID')
    if cardID > -1:
        idStart = cardID + 3
        idEnd = idStart + 16
        userID = res[idStart:idEnd]

    # APIのURL
    url = 'http://192.168.43.226:9999/get'
    
    # APIからユーザデータを取得
    r = requests.get(url)
    users = r.json()
    flg = False
    data = {}

    for user in users:
        if userID == str(user['ID']):
            data = user
            flg = True

    if flg:
        print('ID認証に成功しました。')

    else:
        print('ID認証に失敗しました。')

    return data


# 顔認証を行う関数
def faceAuthentication(userName):
    print('顔認証中...')

    # カメラ撮影
    os.system('wget -O ./../face-app/html/images/capture.jpg http://admin_teamb:qwaszx1212@192.168.43.203:55555/?action=snapshot')

    # 撮影画像をS3へアップロード
    bucket_name='バケット名'
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.upload_file('./../face-app/html/images/capture.jpg','capture.jpg')

    # 顔比較
    rekognition=boto3.client('rekognition')
    SOURCE_IMAGE=userName
    TARGET_IMAGE='capture.jpg'

    def compare():
        res=rekognition.compare_faces(
            SourceImage={
                'S3Object':{
                    'Bucket': bucket_name,
                    'Name': SOURCE_IMAGE,
                }
            },
            TargetImage={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': TARGET_IMAGE,
                }
            },
            SimilarityThreshold=85
        )
        return res['SourceImageFace'], res['FaceMatches']

    # 顔が一致したかどうかの判定
    def similarity():
        source_face, ans = compare()

        for match in ans:
            if match['Similarity']:
                print('OK')
                return True

        print('NG')
        return False

    return similarity()
    

# LogをAPIに送信する関数
def logRegistration(user, deliberation, status):
    print('LogをDBに登録中...')
    
    # APIのURL
    url = 'http://192.168.43.226:9999/post'
    
    # 送信データの組み立てとAPIへの送信
    send_data = {'Name': user['Name'], 'Number': user['ID'], 'Result': deliberation, 'Status': status}
    data = json.dumps(send_data)
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data, headers=headers)
    
    # レスポンスの表示
    print(r.text)


# APIに対して顔の画像名と顔の一致率の送信
def faceMatch(image, num):
    print('一致率を送信中...')
    
    # APIのURL
    url = 'http://192.168.43.203:9999/post'
    
    # 送信データの組み立てとAPIへの送信
    send_data = {'Image': image, 'Match': num}
    data = json.dumps(send_data)
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data, headers=headers)
    
    # レスポンスの表示
    print(r.text)


# LINEで管理者に通知する
def sendLINE():
        url = 'URL'
	channel_access_token = 'TOKEN'
	user_id = 'USER_ID'
	data = {
    		'to' : user_id,
    		'messages' : [
        		{
            			'type' : 'text',
            			'text' : '違反を検知しました'
        		}
    		]
	}
	jsonstr = json.dumps(data)
	print(jsonstr)

	request = urllib2.Request(url, data=jsonstr)
	request.add_header('Content-Type', 'application/json')
	request.add_header('Authorization', 'Bearer ' + channel_access_token)
	request.get_method = lambda: 'POST'
	response = urllib2.urlopen(request)
	ret = response.read()
	print('Response:', ret)
