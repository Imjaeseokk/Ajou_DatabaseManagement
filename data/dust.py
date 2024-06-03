# Python3 샘플 코드 #


import requests
import json
from datetime import datetime

now = datetime.now()
current_date = now.date()
current_time = str(now.time())

print(current_date, current_time)
key = "NhFh8ru3INq1eFM4emIf2BT+nJLQFn8Tq3BrVM1oyGxU/DVxkNHuoDAN+BFszkGPZ5YOBf78fLi/mQK8T0Dmgg=="
url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustFrcstDspth'
params ={'serviceKey' : key, 'returnType' : 'json', 'searchDate' : current_date }

response = requests.get(url, params=params)
data = json.loads(response.content)


# 응답에서 필요한 정보 추출
if data['response']['header']['resultCode'] == '00':
    items = data['response']['body']['items']
    for item in items:
        informCode = item.get('informCode')
        informData = item.get('informData')
        informGrade = item.get('informGrade')
        informCause = item.get('informCause')
        informOverall = item.get('informOverall')
        dataTime = item.get('dataTime')
        imageUrl1 = item.get('imageUrl1')
        imageUrl2 = item.get('imageUrl2')
        imageUrl3 = item.get('imageUrl3')
        if int(current_time[:2]) >= 11 and int(dataTime[-6:-4]) == 11:
            print(f"Inform Code: {informCode}")
            print(f"Inform Data: {informData}")
            print(f"Inform Grade: {informGrade}")
            print(f"Inform Cause: {informCause}")
            print(f"Inform Overall: {informOverall}")
            print(f"Data Time: {dataTime}")
            # print(f"Image URL 1: {imageUrl1}")
            # print(f"Image URL 2: {imageUrl2}")
            # print(f"Image URL 3: {imageUrl3}")
            print("\n")
        elif int(current_time[:2]) <= 11 and int(dataTime[-6:-4]) == 5:
            print(f"Inform Code: {informCode}")
            print(f"Inform Data: {informData}")
            print(f"Inform Grade: {informGrade}")
            print(f"Inform Cause: {informCause}")
            print(f"Inform Overall: {informOverall}")
            print(f"Data Time: {dataTime}")
            # print(f"Image URL 1: {imageUrl1}")
            # print(f"Image URL 2: {imageUrl2}")
            # print(f"Image URL 3: {imageUrl3}")
            print("\n")

else:
    print("Error in response: ", data['response']['header']['resultMsg'])