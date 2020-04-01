from flask import Flask
from flask import render_template
from flask import request

import logging
import sqlite3
from sqlite3 import Error
import io
import csv
from werkzeug.wrappers import Response
from flask import make_response
from flask_csv import send_csv

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


# We create a Flask app
app = Flask(__name__)

# We establish a Flask route so that we can serve HTTP traffic on that route
@app.route('/')
def home():
    # We hardcode some information to be returned
    return "hello world"

@app.route('/chart', methods=['GET', 'POST'])
def chart():
    print("@app.route('/chart')")
    #http://10.1.1.1:5000/chart?stock_code=foo&start_date=bar&end_date=blah
    stock_code = request.args.get('stock_code')
    print("stock_code:", stock_code)
    start_date = request.args.get('start_date')
    print("start_date:", start_date)
    end_date = request.args.get('end_date')
    print("end_date:", end_date)
    values = {'stock_code':stock_code, 'start_date':start_date, 'end_date':end_date}
    print("values:", values)
    return render_template('load_csv.html', values=values)

# We establish a Flask route so that we can serve HTTP traffic on that route
@app.route('/test1')
def weather():
    # We hardcode some information to be returned
    return "{'Temperature': '50'}"

@app.route('/test2/<date>')
def weather_date(date):
    return "date="+date

@app.route('/form')
def form():
    form = getPricesForm()
    return render_template('getPrices.html', title='getPrices', form=form)

@app.route('/api', methods=['GET', 'POST'])
def get_stock_data():
    print("route @app.route('/api')")
    stock_code = request.args.get('stock_code')
    print("stock_code:", stock_code)
    start_date = request.args.get('start_date')
    print("start_date:", start_date)
    end_date = request.args.get('end_date')
    print("end_date:", end_date)
    values = {'stock_code':stock_code, 'start_date':start_date, 'end_date':end_date}
    print("values:", values)
    try:
        # create a database connection
        database = "../asx_data.db"
        print("connecting to database:", database)
        conn = create_connection(database)
        print("connected to database:", database)
        # create tables
        if conn is not None:
            sql = "SELECT * FROM stock_price_yfinance WHERE stock_code = ?"
            print("sql=:", sql)
            cursor = conn.cursor()
            cursor.execute(sql, (stock_code, ) )
            results = cursor.fetchall()
            output = io.StringIO()
            writer = csv.writer(output)
            line = ['stock_code', 'date_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock_Splits']
            writer.writerow(line)
            for result in results:
                print(result)
                writer.writerow(result)
            output.seek(0)
            conn.close()
            #try this
            output = make_response(output.getvalue())
            output.headers["Content-Disposition"] = "attachment; filename=output.csv"
            output.headers["Content-type"] = "text/csv"
            return output
            #return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=output.csv"})
    except Exception as e:
        print("error in route /api/stock_code")
        print(e)
        return "error"



@app.route('/api2/<stock_code>')
def get_stock_data2(stock_code):
    print("route @app.route('/api2/stock_code')")
    print("stock_code=", stock_code)
    try:
        # create a database connection
        database = "../asx_data.db"
        print("connecting to database:", database)
        conn = create_connection(database)
        print("connected to database:", database)
        # create tables
        if conn is not None:
            sql = "SELECT * FROM stock_price_yfinance WHERE stock_code = ?"
            print("sql=:", sql)
            cursor = conn.cursor()
            cursor.execute(sql, (stock_code, ) )
            results = cursor.fetchall()
            csv_list = []
            colnames = ['stock_code', 'date_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock_Splits']
            for result in results:
                print("result:", result)
                dictionary = dict(zip(colnames, list(result) ))
                print("dictionary:", dictionary)
            #writer.writerow(line)
            conn.close()
            #try this
            return "sql completed"

            '''
            colnames = ['stock_code, date_time, Open, High, Low, Close, Volume, Dividends, Stock_Splits']
            result=list( ('BHP.AX', '2020-03-26 15:07:58+11:00', 31.25, 31.25, 31.25, 31.25, 0, 0.0, 0.0))
            '''



            output = make_response(output.getvalue())
            output.headers["Content-Disposition"] = "attachment; filename=output.csv"
            output.headers["Content-type"] = "text/csv"
            return output
            #return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=output.csv"})
    except Exception as e:
        print("error in route /api/stock_code")
        print(e)
        return "error"


# Get setup so that if we call the app directly (and it isn't being imported elsewhere)
# it will then run the app with the debug mode as True
# More info - https://docs.python.org/3/library/__main__.html
if __name__ == '__main__':
    app.run(debug=True)
