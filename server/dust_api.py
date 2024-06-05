import requests
import json
from datetime import datetime

def get_dust_forecast():
    now = datetime.now()
    current_date = now.date()
    current_time = str(now.time())

    key = "NhFh8ru3INq1eFM4emIf2BT+nJLQFn8Tq3BrVM1oyGxU/DVxkNHuoDAN+BFszkGPZ5YOBf78fLi/mQK8T0Dmgg=="
    url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustFrcstDspth'
    params = {'serviceKey': key, 'returnType': 'json', 'searchDate': current_date}

    response = requests.get(url, params=params)
    data = json.loads(response.content)

    pm10_data = {}
    pm25_data = {}
    o3_data = {}
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

            # if (int(current_time[:2]) >= 11 and int(dataTime[-6:-4]) == 11) or (int(current_time[:2]) < 11 and int(dataTime[-6:-4]) == 5):
            if int(current_time[:2]) >= int(dataTime[-6:-4]):
                regions = [region.split(':')[0].strip() for region in informGrade.split(',')]
                grades = [region.split(':')[1].strip() for region in informGrade.split(',')]
                for region, grade in zip(regions, grades):
                    if informCode == 'PM10':
                        pm10_data[region] = {
                            "date": informData,
                            "grade": grade,
                            "cause": informCause,
                            "overall": informOverall
                        }
                    elif informCode == 'PM25':
                        pm25_data[region] = {
                            "date": informData,
                            "grade": grade,
                            "cause": informCause,
                            "overall": informOverall
                        }
                    elif informCode == 'O3':
                        o3_data[region] = {
                            "date": informData,
                            "grade": grade,
                            "cause": informCause,
                            "overall": informOverall
                        }

    # PM10 데이터를 우선으로, 없으면 PM25 데이터를 사용
    results = []
    for region in pm10_data:
        result = {
            "date": pm10_data[region]['date'],
            "region": region,
            "pm10": pm10_data[region]['grade'],
            "ozone": o3_data.get(region, {}).get('grade', 'N/A')
        }
        results.append(result)

    for region in pm25_data:
        if region not in pm10_data:
            result = {
                "date": pm25_data[region]['date'],
                "region": region,
                "pm10": pm25_data[region]['grade'],
                "ozone": o3_data.get(region, {}).get('grade', 'N/A')
            }
            results.append(result)

    return results

print(get_dust_forecast())