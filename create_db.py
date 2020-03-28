import sqlite3
from sqlite3 import Error


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


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "asx_data.db"
    sql_create_asx300_table = """ CREATE TABLE IF NOT EXISTS asx300 (
                                        stock_code text PRIMARY KEY,
                                        stock_name text NOT NULL
                                    ); """
    sql_create_commodity_futures_table = """ CREATE TABLE IF NOT EXISTS commodity_futures (
                                        stock_code text PRIMARY KEY,
                                        stock_name text NOT NULL
                                    ); """
    sql_create_indices_table = """ CREATE TABLE IF NOT EXISTS indices (
                                        stock_code text PRIMARY KEY,
                                        stock_name text NOT NULL
                                    ); """

    sql_create_price_deltas = """ CREATE TABLE IF NOT EXISTS price_deltas (
                                        stock_code text,
                                        min_price real,
                                        min_date_time timestamp,
                                        max_price real,
                                        max_date_time timestamp,
                                        start_period timestamp,
                                        end_period timestamp,
                                        PRIMARY KEY(stock_code, start_period, end_period)
                                    ); """

    sql_create_stock_price_table = """ CREATE TABLE IF NOT EXISTS stock_price_yfinance (
                                        stock_code text,
                                        date_time timestamp,
                                        Open real,
                                        High real,
                                        Low real,
                                        Close real,
                                        Volume integer,
                                        Dividends real,
                                        Stock_Splits real,
                                        PRIMARY KEY(stock_code, date_time)
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_asx300_table)
        create_table(conn, sql_create_stock_price_table)
        create_table(conn, sql_create_commodity_futures_table)
        create_table(conn, sql_create_indices_table)
        create_table(conn, sql_create_price_deltas)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
