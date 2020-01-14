import mysql.connector as sql
from mysql.connector import Error
import time


def dbquerry(string):
    try:
        db = sql.connect(
        host="192.168.1.4",
        user="root",
        passwd="root",
        database="ceneco_old")
        if(db.is_connected()):
            dbcursor = db.cursor(dictionary=True)
            dbcursor.execute(string)
            if ("SELECT" in string.upper()[:6]):
                x= dbcursor.fetchall()
                return x
                # for key in x:
                #     results.append(key)
                #     print(key)
            if("INSERT" in string.upper()[:6]):
                print('here')
                db.commit()
            elif("UPDATE" in string.upper()[:6]):
                db.commit()
    except Error as e:
        print(e)