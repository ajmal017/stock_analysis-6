import sqlite3
from sqlite3 import Error
import pandas as pd

'''
python load_indices.py
verify data entered after running
sqlite3 asx_data.db
SELECT COUNT(*) FROM asx300;
will get 296 rows - since asx 300 .csv file only has 297 rows including header
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

def get_codes(database, stock_codes_filename, dest_table):
    conn = create_connection(database)
    # create tables
    if conn is not None:
        # create projects table
        print("load list from csv, insert data to database.")
        data = pd.read_csv(stock_codes_filename)
        print("data.shape:", data.shape)
        print("data.head()\n")
        print(data.head())
        print("data.columns: ", data.columns)
        #data.columns=["Code","Company","Sector","Market","Cap", "Weight(%)"]
        #df = data[["Code","Company"]]
        df = data.iloc[:, 0:2]
        print("after truncating > df.head()\n")
        print(df.head())
        #dataframe.to_sql creates error if table already exists. replace
        #df.to_sql('asx300', con=conn)
        cursor=conn.cursor
        for i,row in df.iterrows():
            print("i:", i)
            print("type(row):", type(row))
            print("row:", row)
            sql = "INSERT INTO "+dest_table+"(stock_code, stock_name) VALUES (?, ?)"
            try:
                conn.execute(sql, tuple(row))
            except Exception as e:
                print("error inserting :", str(e))
        conn.commit()
        print("list from csv added.")
    else:
        print("Error! cannot create the database connection.")



def main():
    get_codes("asx_data.db", "data/commodities_futures.csv", "commodity_futures")
    get_codes("asx_data.db", "data/global_indices.csv", "indices")





if __name__ == '__main__':
    main()
