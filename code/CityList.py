#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import requests
import json , re
import mysql.connector

conn = mysql.connector.connect(user='root', password='root', database='Utils')



def getCityGeo(cityname):
    url = 'http://ditu.amap.com/service/poiInfo?query_type=TQUERY&keywords=%s' % (cityname)
    html = requests.get(url).text
    print html

    if len(html) < len('{"status":"2","data":"Return Failure!"12312323}') :
        return -1

    data = json.loads(html)
    cityList = []
    try:
        searchList = data['data']['locres']['poi_list']
        # searchList = data['data']['poi_list']
        # city = searchList[0]
        # _city = {'level': '', 'child_station_count': city['child_station_count'],
        #          'adcode': city['adcode'], 'coords': '', 'address': city['address'],
        #          'ename': '', 'name': city['name'], 'longitude': city['longitude'],
        #          'latitude': city['latitude']}
        # return _city
        for city in searchList:
            _city = { 'level' : city['level'] , 'child_station_count' : city['child_station_count'],
                     'adcode': city['adcode'] , 'coords' : city['coords'] , 'address' : city['address'],
                     'ename' : city['ename'], 'name' : city['name'] , 'longitude' : city['longitude'],
                      'latitude': city['latitude']}
            return _city
    except Exception:
        return cityList


def saveInfo(cityInfo , city):
    if cityInfo < 3:
        print city + 'not include'
        return
    print  city
    try:
        print cityInfo['ename']
        cursor = conn.cursor()
        tem = cityInfo['ename']
        tem = str(tem).replace('\'' , '`')
        _sql = 'insert into CityGeo(ename , name , level , adcode ,child_station_count,coords ,  address , longitude ,latitude ) values (\'%s\',\'%s\',\'%s\',\'%s\',%s, \'%s\' ,\'%s\' ,\'%s\', \'%s\')' % (
            tem, city, cityInfo['level'], cityInfo['adcode'], cityInfo['child_station_count'],
            # cityInfo['coords'] ,
            "",
            cityInfo['address'] ,cityInfo['longitude'] ,cityInfo['latitude'])
        print(_sql)
        cursor.execute(_sql)
        conn.commit()
    except Exception:
        with open('errorcity' ,'a') as f:
            # print city
            f.write(city + '\n')
        print (city + 'error')





def getCityListDB():
    cursor = conn.cursor()
    _sql = 'SELECT `ChinaCity`.`cityName`,`ChinaCity`.`regionName` FROM `ChinaCity` WHERE `ChinaCity`.`cityName` != \'\' and id > 248'
    cursor.execute(_sql)
    cityList = cursor.fetchall()

    for city in cityList:
        if len(city) > 1:
            if '盟' in city[0]:
                temp = city[0]  + city[1]
            else:
                temp = city[0] + u'市' + city[1]
        else:
            temp = city[0] + u'市'
        print temp
        saveInfo( getCityGeo(temp) , temp)

def  getCityListText():
    with open('citylist' , 'r') as f:
        cityList = f.readlines()

    for city in cityList:
        city = city.strip()
        # city = city + '县'
        saveInfo(getCityGeo(city), city)


getCityListText()

# getCityListDB()
# getCityGeo('北京')