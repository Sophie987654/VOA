import requests
import json
import pandas as pd
from pandas import json_normalize
from settings import *
from src.module.TAGO_data import *
from src.module.tts import *

key = "0xs+oSKQksWdfMFsi+mP8Tuc9/xe+e6oqMRn4St5c0ffbe7SsWaeaMwR3LICld+RNhOJArZ/G4W5bFkZB18wEw=="
global flag
flag = False
global trainInfoDf, new_df

def res(url, params):
    response = requests.get(url, params=params)
    text = response.text

    data = json.loads(text)
    df = json_normalize(data['response']['body']['items']['item'])
    
    global flag
    if (flag):
        global trainInfoDf, new_df
        trainInfoDf = df
        new_df = pd.DataFrame(columns = trainInfoDf.columns)

#-------------- 도시코드 목록 조회 --------------
def cityCode():
    url = 'http://apis.data.go.kr/1613000/TrainInfoService/getCtyCodeList'
    params = {'serviceKey' : key, '_type' : 'json' }

    res(url, params)

#-------------- 시도별 기차역 목록 조회 --------------
def trainStation():
    cityCode = "37"

    url = 'http://apis.data.go.kr/1613000/TrainInfoService/getCtyAcctoTrainSttnList'
    params ={'serviceKey' : key,
            'pageNo' : '1', 'numOfRows' : '100', '_type' : 'json',
            'cityCode' : cityCode }

    res(url, params)

#-------------- 차랑종류 목록 조회 --------------
def vhcleKnd():
    url = 'http://apis.data.go.kr/1613000/TrainInfoService/getVhcleKndList'
    params ={'serviceKey' : key, '_type' : 'json' }

    res(url, params)

#-------------- 출도착지 기반 열차 정보 조회 --------------
def trainInfo(dep, arr, depDay):
    depPlaceId = dep    #출발지ID
    arrPlaceId = arr    #도착지ID
    depPlandTime = depDay   #출발일
    # trainGradeCode = knd   #차량종류코드
    
    url = 'http://apis.data.go.kr/1613000/TrainInfoService/getStrtpntAlocFndTrainInfo'
    
    if gVar.currentP == "selStation":
        params ={'serviceKey' : key,
                'pageNo' : '1', 'numOfRows' : '1', '_type' : 'json',
                'depPlaceId' : depPlaceId, 'arrPlaceId' : arrPlaceId,
                'depPlandTime' : depPlandTime }
    else:
        params ={'serviceKey' : key,
                'pageNo' : '1', 'numOfRows' : '100', '_type' : 'json',
                'depPlaceId' : depPlaceId, 'arrPlaceId' : arrPlaceId,
                'depPlandTime' : depPlandTime} # , 'trainGradeCode' : trainGradeCode }

    try:
        res(url, params)
        return True
    except:
        print("오류")
        return False


def isExist(depStat, arrStat, depDay):
    global flag, trainInfoDf
    
    try:
        dep = station[depStat]
        arr = station[arrStat]
        # knd = trainKnd[knd]

        flag = False
        if trainInfo(dep, arr, depDay):
            return True
        else:
            return False
    except:
        print("오류")
        return False

def getData(depStat, arrStat, depDay, depTime):
    global flag, trainInfoDf, new_df
    
    dep = station[depStat]
    arr = station[arrStat]
    # knd = trainKnd[knd]

    flag = True
    if trainInfo(dep, arr, depDay):
        deptimeList = trainInfoDf['depplandtime'].tolist()
        timeDiff = list()

        i = 0
        for time in deptimeList:
            if gVar.mode == "touch":
                hour = str(time)[8:10]
                
                if hour == depTime[0:2]:
                    time1 = datetime(int(str(time)[0:4]), int(str(time)[4:6]), int(str(time)[6:8]),
                                int(str(time)[8:10]), int(str(time)[10:12]), 0)
                    if (time1 - datetime.now()).total_seconds() >= 0:
                        new_df = new_df._append(trainInfoDf.iloc[i])
            
            elif gVar.mode == "voice":
                time1 = datetime(int(str(time)[0:4]), int(str(time)[4:6]), int(str(time)[6:8]),
                                int(str(time)[8:10]), int(str(time)[10:12]), 0)
                time2 = datetime(int(depDay[0:4]), int(depDay[4:6]), int(depDay[6:8]),
                                int(depTime[0:2]), int(depTime[2:4]), 0)
                if (time1 - datetime.now()).total_seconds() >= 0:
                    timeDiff.append([i, abs((time1 - time2).total_seconds())])

            i += 1

        if gVar.mode == "voice":
            timeDiff.sort(key=lambda x: (x[1], x[0]))
            new_df = new_df._append(trainInfoDf.iloc[timeDiff[0][0]])
            new_df = new_df._append(trainInfoDf.iloc[timeDiff[1][0]])
        
        # 빈 행 제거
        new_df = new_df.dropna()
        # 인덱스 재설정
        new_df = new_df.reset_index(drop=True)

        return new_df
    else:
        empty_df = pd.DataFrame()
        return empty_df