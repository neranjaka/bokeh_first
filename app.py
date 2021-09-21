from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure, show
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import numpy as np
import requests

app = Flask(__name__)

key = open('API_KEY.txt').read()
stock_code = 'TSLA'

print(np.__version__)

def read_stock(key,stock_code):
    ts = TimeSeries(key, output_format='pandas')
    #data, meta = ts.get_intraday(stock_code, interval = '1min', outputsize = 'full')
    data, meta = ts.get_daily_adjusted(stock_code, outputsize = 'full')

    columns = ['Open','High','Low','Close','Adjusted_Close','Volume','Dividend_Amount','Split_Coefficient']
    data.columns = columns

    data_date = [date for date in data.index]
    data_date.reverse()

    data_close_price = [float(data["Close"][date]) for date in data.index]
    data_close_price.reverse()
    data_close_price = np.array(data_close_price)


    return data_date,data_close_price


#print(data.info())

#date = data.index
#high = data['4. close']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')
    #return render_template('create_graph.html')

@app.route('/stock')
def create_graph():

        data_date, data_close_price = read_stock(key,stock_code)
        x = data_date
        y = data_close_price

        # create a new plot with a title and axis labels
        p = figure(title="Closing Prices", x_axis_label='Date', y_axis_label='Closing Price')

        # add a line renderer with legend and line thickness to the plot
        p.line(x, y, line_width=2)

        # show the results
        show(p)
        return render_template('index.html')

if __name__ == '__main__':
    app.run(port=33507)
