import sqlite3
from sqlite3 import Error
import pandas as pd
import datetime
import yfinance as yf


'''
'''

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def get_prices(database, start, end, tablename, code_suffix):
    # create a database connection
    conn = create_connection(database)
    # create tables
    if conn is not None:
        #get list of stock codes from db
        sql = "SELECT * FROM "+tablename
        cursor=conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            print(i[0], i[1])
            #retrieve data with yfinance for each stock code.
            stock_code = i[0]+code_suffix
            print("stock_code:", stock_code)
            try:
                msft = yf.Ticker(stock_code)
                print("msft:", msft)
                print(msft.info)
                #print(msft.info.keys())
                #print("bookValue : ", msft.info['bookValue'])
                #print("volume24Hr = ",msft.info['previousClose'])
                #nbb: if using interval="1h" datetime returned is all same time for the same day. weird bug?
                result = msft.history(start = start, end = end, interval="60m")
                print("history > result\n", result)
                #print(type(result)) #pandas.dataframe
                cursor=conn.cursor
                for i,row in result.iterrows():
                    print("i:", i)
                    print("type(i):", type(i))
                    print("type(row):", type(row))
                    print("row:\n", row)
                    sql = "INSERT INTO stock_price_yfinance(" \
                        +" stock_code, date_time, Open, High, Low , Close, "\
                        +" Volume, Dividends, Stock_Splits) "\
                        +" VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                    print("sql=:", sql)
                    print(tuple(row))
                    values = list(row)
                    print("type(values):", type(values))
                    print(values)
                    values = [stock_code, str(i)]+values
                    print("after adding stock code + time, type(values):", type(values))
                    print(values)
                    try:
                        conn.execute(sql, tuple(values))
                    except Exception as error:
                        print("error inserting data: ", str(error))
                conn.commit()
            except Exception as error:
                print("error retrieving yfinance data: ", str(error))
            else:
                print("yfinance data retrieved.")
        # store data in db


def main():
    database = "asx_data.db"
    #start = datetime.datetime(2020, 3, 25, 0, 0)
    #end   = datetime.datetime(2020, 3, 26, 20, 0)

    end = datetime.datetime.now()
    start = end - datetime.timedelta(hours=24)
    #now trim start to get start of day for previous day.
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)

    get_prices(database, start, end, "asx300", ".AX")
    #start = datetime.datetime(2020, 3, 1,  20, 0)
    #end   = datetime.datetime(2020, 3, 26, 20, 0)
    get_prices(database, start, end, "commodity_futures", "")
    get_prices(database, start, end, "indices", "")



if __name__ == '__main__':
    main()
