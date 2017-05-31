import http.client, urllib.parse
import configparser
import logging
#import sys
import codecs
import re
from models import Tracking, ModelTrack
import psycopg2
from dbconnector import BaseConnector
from datetime import date
from datetime import datetime


"""
包裹追踪类
"""
class Tracker(object):

    def run(self):
        conn = http.client.HTTPConnection("www.laposte.fr")
        conn.request("GET", "/particulier/outils/suivre-vos-envois?code=EY216209619FR")
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        data1 = r1.read()
        print(len(data1))
        #logging.debug(str(data1,'utf-8'))
        # 1. 先找出记录表格；2. 然后逐条提取每行记录。
        epTable = re.compile('(<table.*?>(.+?)Résultats pour(.+?)</table>)', re.IGNORECASE)
        epLine = re.compile('<p class="h5">((.|\w)*?)</p>', re.IGNORECASE)
        #result = ep.match(str(data1, 'utf-8'))
        eReference = re.compile('Envoi n° ([A-Z]{2}[0-9]{9}[A-Z]{2}) - Colissimo', re.IGNORECASE)
        eDestination = re.compile('Destination :((\s|[a-zA-Z])+)', re.IGNORECASE)
        tabBlock = re.findall(epTable, str(data1, 'utf-8'))
        if (tabBlock is not None):
            #print(tabBlock[0])
            tabBlockStr = tabBlock[0][0]
            #print(tabBlockStr)
            #print(type(tabBlockStr))
            lineBlock = re.findall(epLine, tabBlockStr)
            if (lineBlock is None):
                logging.debug("Can't capture line from table result")
                return
            item = 0
            
            # 匹配包裹号
            parcelReference = re.findall(eReference, str(data1, 'utf-8'))
            if (parcelReference is not None):
                print("reference: " + parcelReference[0])
            
            # 匹配出收件城市
            parcelCity = re.findall(eDestination, str(data1, 'utf-8'))
            if (parcelCity is not None):
                print('city: ' + parcelCity[0][0])

            cModelTrack = ModelTrack(parcelReference, parcelCity)
            for index in range(0, int(round(len(lineBlock) / 3))) :
                lineNumber = index * 3
                parcelDate = lineBlock[lineNumber][0]
                parcelStatut = lineBlock[lineNumber + 1][0]
                parcelLocation = lineBlock[lineNumber + 2][0]
                # print( parcelDate + ", " + \
                #         parcelStatut + ", " +
                #         parcelLocation)
                newTrack = Tracking(parcelDate, parcelStatut, parcelLocation)
                cModelTrack.addTracking(newTrack)
            #cModelTrack.printTrack()
            print ("Hello, world!")
            return cModelTrack


"""
读取配置文件
"""
def ConfigSectionMap(section):
    dict1=[]
    Config = configparser.ConfigParser()
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


"""
连接数据库
"""
def ConnectDatabase():
    #Define our connection string
    conn_string = "host='localhost' dbname='vido' user='Lei' password=''"
	# print the connection string we will use to connect
    print("Connecting to database -> %s" % conn_string)
	# get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)
	# conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()

    # Insert one line 
    insertSql = "Insert into "
    cursor.execute(insertSql)


    # Execute our query
    cursor.execute(" SELECT * FROM polls_Parcel ")

    # Retrieve the records from the database
    rows = cursor.fetchall()
    print("\n Rows: \n")
    for row in rows:
        print(" ", row[1])
    print("Printed !")

def GetTrackingSavedInfo(pRefParcel):
    # Test Get info from database
    #Define our connection string
    conn_string = "host='localhost' dbname='vido' user='Lei' password=''"
	# print the connection string we will use to connect
    print("Connecting to database -> %s" % conn_string)
	# get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)
	# conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()

    # Execute our query
    cursor.execute(" SELECT * FROM polls_tracking WHERE reference = '" + pRefParcel + "'")

    # Retrieve the records from the database
    rows = cursor.fetchall()

    cModelTrack = ModelTrack(pRefParcel)    
    #print("\n Rows: \n")
    for row in rows:
        newTrack = Tracking(row[3], row[4], row[5]) 
        print("ref:  %s, date: %s, status: $s, location: %s", row[1], row[3], row[4], row[5])
        cModelTrack.addTracking(newTrack)
    return cModelTrack
    # End Test dataBase


"""
主函数
"""
if __name__ == '__main__':
    logging.basicConfig(filename='example.log',level=logging.DEBUG)
    #logging.basicConfig(handlers=[logging.FileHandler('example2.log', 'w', 'utf-8')], level=logging.DEBUG)
    logging.basicConfig(format='%(asctime)s %(message)s')

    # logging.debug('This message should go to the log file')
    # logging.info('So should this')
    # logging.warning('And this, too')

    config = configparser.ConfigParser()
    config.read("config.ini")
    sitePoste = config.get("La Poste", "site")
    #ConnectDatabase()
    #baseCon = BaseConnector('Lei', '', 'vido')
    #baseCon.connect()





    
    # 从网站找出所有包裹记录, 返回网站中所有记录行.
    parcel_tracking = Tracker().run()
    
    # 从数据库读取记录
    parcel_tracking_saved = GetTrackingSavedInfo(parcel_tracking.refParcel)

    # 对比网站里的记录和数据库中已经存储的记录，把新记录存在数据库中。
    '''
    if parcel_tracking is not None:
        parcel_ref = parcel_tracking.refParcel
        parcel_destination = parcel_tracking.destination
        for line in parcel_tracking.lstTracking:
            date_str = line.parcelDate
            my_date = datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
            #print(parcel_ref, my_date, line.parcelStatut, line.parcelLocation)
            #statut_bytes = line.parcelStatut.encode('utf8')
            #print(type(st))
            baseCon.insert_parcel_tracking(parcel_ref, parcel_destination, my_date, line.parcelStatut, line.parcelLocation)
            baseCon.display_record(None)
    '''