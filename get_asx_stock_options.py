import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions # available since 2.26.0
from selenium.webdriver.support import expected_conditions # available since 2.26.0
from selenium.webdriver.common.by import By
import pandas as pd

import sqlite3
from sqlite3 import Error
import pandas as pd
import datetime

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

def scrape_asx(stock_code, today):
    chromedriver = "D:/2020/coding/stock_analysis/chrome_drivers/chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    browser = webdriver.Chrome(chromedriver)
    try:
        browser.get('https://www.asx.com.au/asx/markets/optionPrices.do')
        formElem = browser.find_element_by_id('underlyingCode')
        formElem.send_keys(stock_code)
        submitButton = browser.find_element_by_id('submit')
        submitButton.click()
        colnames = ['code', 'expiry_date', 'put_call', 'exercise', 'bin', 'offer', 'last', 'volume', 'open_interest', 'margin_price']
        df = pd.DataFrame(columns=colnames)
        optionsTableElement = browser.find_element_by_id('optionstable')
        type(optionsTableElement)
        rows = optionsTableElement.find_elements_by_tag_name('tr')
        for row in rows[1:]:
            print(row)
            row_values = []
            cells_stockcode = row.find_elements_by_tag_name("th")[0].text
            row_values.append(cells_stockcode)
            #print("cells_stockcode:", cells_stockcode)
            cells = row.find_elements_by_tag_name("td")
            #print(type(cells), len(cells))
            for cell in cells:
                print(cell.text)
                row_values.append(cell.text)
            print("row_values:", row_values)
            a_series = pd.Series(row_values, index = df.columns)
            df = df.append(a_series, ignore_index=True)
            print("df.shape:", df.shape)
            #break
        file_out_prefix = stock_code+"_options_"+today.strftime("%Y_%m_%d")
        #dynamically construct this w stock code and date of run
        print("saving dataframe to file "+file_out_prefix+".zip")
        compression_opts = dict(method='zip', archive_name=file_out_prefix+'.csv')
        df.to_csv("data_collected/"+file_out_prefix+".zip", index=False, compression=compression_opts)
    except Exception as e:
        print("error", str(e))
    browser.quit()


def get_options(database, tablename):
    # create a database connection
    conn = create_connection(database)
    today = datetime.datetime.now()
    today.replace(hour=0, minute=0, second=0, microsecond=0)
    print("today:", today.strftime("%Y_%m_%d"))
    # create tables
    if conn is not None:
        #get list of stock codes from db
        sql = "SELECT * FROM "+tablename
        cursor=conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        count =0
        for result in results:
            count = count+1
            stock_code = result[0]
            print("stock_code:", stock_code)
            scrape_asx(stock_code, today)
            #if count > 5:
            #    break



def main():
    database = "asx_data.db"
    get_options(database, "asx300")



if __name__ == '__main__':
    main()
