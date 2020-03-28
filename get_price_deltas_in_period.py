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

def find_min_max(database, start, end, tablename, code_suffix):
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
            sql_min = "SELECT date_time, min(open) as min_open FROM stock_price_yfinance WHERE stock_code='"+stock_code+"' AND date_time >= '"+str(start)+"'";
            sql_max = "SELECT date_time, max(open) as max_open FROM stock_price_yfinance WHERE stock_code='"+stock_code+"' AND date_time <= '"+str(end)+"'";
            try:
                print("sql_min:", sql_min)
                cursor.execute(sql_min)
                result = cursor.fetchone()
                print("type(result):", type(result))
                print ("result:", result)
                min_price = result[1]
                min_date_time = result[0]
                print("sql_max:", sql_max)
                cursor.execute(sql_max)
                result = cursor.fetchone()
                print ("result:", result)
                max_price = result[1]
                max_date_time = result[0]
                print(stock_code+": min:"+str(min_price)+" @ "+ str(min_date_time) + "  max: "+str(max_price)+" @ "+str(max_date_time) )
                if max_price!=None and min_price!=None:
                    sql = "INSERT INTO price_deltas (stock_code, " \
                        + "min_price, min_date_time, max_price, " \
                        + "max_date_time, start_period, end_period )" \
                        +" VALUES (?, ?, ?, ?, ?, ?, ?)"
                    print("sql=:", sql)
                    values = (stock_code, min_price, min_date_time, max_price, max_date_time, start, end)
                    print("values=:", values)
                    try:
                        conn.execute(sql, tuple(values))
                    except Exception as error:
                        print("error inserting data: ", str(error))
                else:
                    print("no results for stock code ", stock_code)
            except Exception as error:
                print("error retrieving data: ", str(error))
        conn.commit()


def main():
    database = "asx_data.db"
    start = datetime.datetime(2020, 3, 26, 0, 0)
    end   = datetime.datetime(2020, 3, 26, 20, 0)
    #or use timedelta to get last 24hrs.
    end = datetime.datetime.now()
    start = end - datetime.timedelta(hours=24)
    #now trim start to get start of day for previous day.
    start.replace(hour=0, minute=0, second=0, microsecond=0)
    #
    tablename = "asx300"
    code_suffix=".AX"
    find_min_max(database, start, end, tablename, code_suffix)
    #
    tablename = "indices"
    code_suffix=""
    find_min_max(database, start, end, tablename, code_suffix)
    #
    tablename = "commodity_futures"
    code_suffix=""
    find_min_max(database, start, end, tablename, code_suffix)


if __name__ == '__main__':
    main()
