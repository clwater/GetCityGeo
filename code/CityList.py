#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json , re
# import mysql.connector

# conn = mysql.connector.connect(user='root', password='root', database='Utils')



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
    # with open('citylistshort' , 'r') as file:
    with open('citylist' , 'r') as file:
        cityList = file.readlines()

    provinceId = 0
    cityId =  0
    regionId = 0

    for city in cityList:
        city = city.replace('Region' , ' Region')
        city = city.strip()
        city = city + ' '





        if 'Region'  in city :
            regionId = regionId + 1
        elif 'City' in city :
            regionId = 0
            cityId = cityId + 1
        else:
            regionId = 0
            cityId = 0
            provinceId = provinceId + 1




        provinceName = re.findall('Province: .*? ' , city)
        provinceName = provinceName[0]
        provinceName = provinceName.replace('Province: ' , '')
        provinceName = provinceName.strip()



        cityName = re.findall('City: .*? ', city)
        regionName = re.findall('Region: .*? ', city)




        if len(cityName) > 0:
            cityName = cityName[0]
            cityName = cityName.replace('City: ', '')
            cityName = cityName.strip()
            # print cityName

            if len(regionName) > 0:
                regionName = regionName[0]
                regionName = regionName.replace('Region: ', '')
                regionName = regionName.strip()
                # print regionName

                print 'provinceName: ' + provinceName + ' provinceId: ' + str(provinceId) + \
                      ' cityName: ' + cityName + ' cityId: ' + str(cityId) + \
                      ' regionName: ' + regionName + ' regionId: ' + str(regionId)
            else:

                print 'provinceName: ' + provinceName + ' provinceId: ' + str(provinceId) + \
                  ' cityName: ' + cityName + ' cityId: ' + str(cityId)
        else:
            print 'provinceName: ' + provinceName + ' provinceId: ' + str(provinceId)





        # cityListInfo = getCityGeo(city)
    #
    #     for cityInfo in cityListInfo:
    #         print cityInfo
    #         print (cityInfo['ename'])
    #         saveInfo(cityInfo , city)
    #

getCityListText()
# getCityGeo('北京')