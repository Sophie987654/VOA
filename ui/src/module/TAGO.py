import requests
import json
from pandas import json_normalize
from settings import *
from src.module.TAGO_data import *

key = "0xs+oSKQksWdfMFsi+mP8Tuc9/xe+e6oqMRn4St5c0ffbe7SsWaeaMwR3LICld+RNhOJArZ/G4W5bFkZB18wEw=="
global flag
flag = False
global trainInfoDf

def res(url, params):
    response = requests.get(url, params=params)
    text = response.text
    # print(text)

    data = json.loads(text)
    df = json_normalize(data['response']['body']['items']['item'])
    
    global flag
    if (flag):
        global trainInfoDf
        trainInfoDf = df

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
def trainInfo(dep, arr, depDay):#, knd):
    depPlaceId = dep    #출발지ID
    arrPlaceId = arr    #도착지ID
    depPlandTime = depDay   #출발일
    #trainGradeCode = knd   #차량종류코드
    
    url = 'http://apis.data.go.kr/1613000/TrainInfoService/getStrtpntAlocFndTrainInfo'
    
    if gVar.currentP == "selStation":
        params ={'serviceKey' : key,
                'pageNo' : '1', 'numOfRows' : '100', '_type' : 'json',
                'depPlaceId' : depPlaceId, 'arrPlaceId' : arrPlaceId,
                'depPlandTime' : depPlandTime }
    else:
        params ={'serviceKey' : key,
                'pageNo' : '1', 'numOfRows' : '100', '_type' : 'json',
                'depPlaceId' : depPlaceId, 'arrPlaceId' : arrPlaceId,
                'depPlandTime' : depPlandTime}#, 'trainGradeCode' : trainGradeCode }
    
    try:
        res(url, params)
    except:
        gVar.notExist = True
        pass

def getData(depStat, arrStat, depDay, depTime):#, knd):
    global flag, trainInfoDf
    
    dep = station[depStat]
    arr = station[arrStat]
    #knd = trainKnd[knd]

    flag = True
    trainInfo(dep, arr, depDay)#, knd)

    if (gVar.notExist == False):
        deptimeList = trainInfoDf['depplandtime'].tolist()
        # print(deptimeList)
        i = 0
        for time in deptimeList:
            time = int(str(time)[8:12])
            if (time - int(depTime) > 0):
                break
            i += 1

            lastIndex = trainInfoDf.shape[0]
        #print(trainInfoDf.head(lastIndex - i))
        trainInfoDf = trainInfoDf.tail(lastIndex - i)
        trainInfoDf = trainInfoDf.reset_index()
        print(trainInfoDf)
        return trainInfoDf
    
    else:
        pass
