import psycopg2
#import sys
#import logging

class BaseConnector(object):
    """ 数据库操作类 """

    def __init__(self, pUserName, pPWD, pDBName):
        self.user_name = pUserName
        self.pwd = pPWD
        self.db_name = pDBName
        self.conn = None
        self.cursor = None


    def connect(self):
        """ Connect data base """
        conn_string = "host='localhost' dbname='" + self.db_name + "' "
        conn_string += "user='" + self.user_name + "' "
        conn_string += "password='"  + self.pwd + "'"
	    # print the connection string we will use to connect
        print("Connecting to database -> %s" % conn_string)
	    # get a connection, if a connect cannot be made an exception will be raised here
        self.conn = psycopg2.connect(conn_string)
        self.conn.set_client_encoding('utf8')
	    # conn.cursor will return a cursor object, you can use this cursor to perform queries
        self.cursor = self.conn.cursor()
        # Insert one line
        #insertSql = "Insert into "
        #cursor.execute(insertSql)

        # Execute our query
        self.cursor.execute(" SELECT * FROM polls_tracking ")

        # Retrieve the records from the database
        rows = self.cursor.fetchall()
        print("\n Rows: \n")
        for row in rows:
            print(" ", row[1])
        print("display end !")


    def insert_parcel_tracking(self, parcel_reference, parcel_destination, parcel_date, \
        parcel_statut, parcel_location):
        """ 插入包裹追踪信息 """
        #parcel_statut = parcel_statut.encode('utf-8')

        # insert_sql = "INSERT INTO polls_tracking (tracking_reference, tracking_destination, "
        # insert_sql += "tracking_date, tracking_statut, tracking_location) VALUES "
        # insert_sql += "('" + parcel_reference + "', '" + parcel_destination + "', "
        # insert_sql += "'" + parcel_date + "', " + "'" + parcel_statut + "', "
        # insert_sql += "'" + parcel_location + "')"

        insert_sql = "INSERT INTO polls_tracking (tracking_reference, tracking_destination, "
        insert_sql += "tracking_date, tracking_statut, tracking_location) VALUES "
        insert_sql += "(%s, %s, %s, %s, %s);"

        #print(insert_sql, (parcel_reference, parcel_destination, parcel_date, parcel_statut, parcel_location))
        #data = (parcel_reference, parcel_destination, parcel_date, parcel_statut, parcel_location,)
        self.cursor.execute(insert_sql, (parcel_reference, parcel_destination, parcel_date, parcel_statut, parcel_location))
        #self.conn.commit()
        print("Insert parcel tracking is ok")

    def display_record(self, parcel_reference):
        """ 查询包裹信息(以包裹单号为检索) """
        # Execute our query
        print("Print polls_tracking, reference: ", parcel_reference)
        select_sql = ''
        if parcel_reference is None:
            select_sql = "SELECT * FROM polls_tracking"
        else:
            select_sql = "SELECE * FROM polls_tracking "
            select_sql += "WHERE tracking_reference = '" + parcel_reference + "'"
        self.cursor.execute(select_sql)
        # Retrieve the records from the database
        rows = self.cursor.fetchall()
        print("\n parcel tracking Rows: \n")
        for row in rows:
            print(row[1], row[2], row[3], row[4])
        print("Printed !")
