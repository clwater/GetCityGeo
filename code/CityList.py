#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
import mysql.connector

conn = mysql.connector.connect(user='root', password='root', database='Utils')



def getCityGeo(cityname):
    url = 'http://ditu.amap.com/service/poiInfo?query_type=TQUERY&keywords=%s' % (cityname)
    html = requests.get(url).text
    # print html

    data = json.loads(html)
    cityList = []
    try:
        searchList = data['data']['locres']['poi_list']
        for city in searchList:
            _city = { 'level' : city['level'] , 'child_station_count' : city['child_station_count'],
                     'adcode': city['adcode'] , 'coords' : city['coords'] , 'address' : city['address'],
                     'ename' : city['ename'], 'name' : city['name'] , 'longitude' : city['longitude'],
                      'latitude': city['latitude']}
            cityList.append(_city)
        return cityList
    except Exception:
        return cityList


def saveInfo(cityInfo , city):
    try:
        cursor = conn.cursor()
        _sql = 'insert into CityGeo(ename , name , level , adcode ,child_station_count,coords ,  address , longitude ,latitude ) values (\'%s\',\'%s\',\'%s\',\'%s\',%s, \'%s\' ,\'%s\' ,\'%s\', \'%s\')' % (
            cityInfo['ename'], city, cityInfo['level'], cityInfo['adcode'], cityInfo['child_station_count'],
            # cityInfo['coords'] ,
            "",
            cityInfo['address'] ,cityInfo['longitude'] ,cityInfo['latitude'])
        # print(_sql)
        cursor.execute(_sql)
        conn.commit()
    except Exception:
        with open('errorcity' ,'a') as f:
            f.write(city + '\n')
        print (city + 'error')




def getCityListText():
    cityList = []
    with open('citylist' , 'r') as file:
        cityList = file.readlines()

    for city in cityList:
        print (city)
        cityListInfo = getCityGeo(city)

        for cityInfo in cityListInfo:
            print (cityInfo['ename'])
            saveInfo(cityInfo , city)
        

getCityListText()
# getCityGeo('北京')