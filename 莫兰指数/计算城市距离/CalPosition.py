# -*- coding: utf-8 -*-
from geopy.distance import geodesic
import urllib.parse
import hashlib
import requests

ak = "n80sB3TqG2CPCSDVdLHD1v2xXywTqayE"#百度地图ak码
sk = "GXG9uCoq9NNFGVv2pfgaOByx4dOqU9ls"#百度地图sk码

def getCoordinate(address):
    '''
    输入地址输出坐标(经度，维度)
    address：城市名
    '''
    #产生sn码
    queryStr = "/geocoding/v3/?address="+address+'&output=json&ak='+ak
    encodedStr = urllib.parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
    rawStr = encodedStr+sk
    sn = (hashlib.md5(urllib.parse.quote_plus(rawStr).encode("utf8")).hexdigest())
    #生成url
    url = urllib.parse.quote("http://api.map.baidu.com"+queryStr+"&sn="+sn,safe="/:=&?#+!$,;'@()*[]")
    result = requests.get(url).json()
    print(result)
    coordinate = (result['result']['location']['lng'],result['result']['location']['lat'])
    return coordinate

def calDistance(place1,place2):
    '''
    输入两个地点名，输出直线距离(米)
    place1：地点1
    place2：地点2
    '''
    coor1 = getCoordinate(place1)#经纬度1
    coor2 = getCoordinate(place2)#经纬度2
    #这里输入纬度在前，经度在后，所以做一下反转
    distance = geodesic(coor1[::-1],coor2[::-1]).m#距离(米)
    return distance

if __name__ == "__main__":
    # p1 = "北京市"
    # r1 = getCoordinate(p1)
    # print("%s经纬度"%p1,r1)
    # p2 = "重庆市"
    # r2 = getCoordinate(p2)
    # print("%s经纬度"%p2,r2)
    # distance = calDistance(p1,p2)
    # print("两地距离约为%d米"%distance)

    print(calDistance('北京','上海'))