'''
https://pandas-datareader.readthedocs.io/en/latest/remote_data.html
resurrecting old project > https://pandas-datareader.readthedocs.io/en/latest/remote_data.html

https://plotly.com/python/getting-started/
pip install plotly

https://pypi.org/project/pandas-datareader/
pip install pandas-datareader

https://pydata.github.io/pandas-datareader/


https://pypi.org/project/chart-studio/
pip install chart-studio
'''
#--new----------------
from pandas_datareader import data, wb
import pandas_datareader as pdr
from datetime import datetime
start = datetime(2020, 3, 25)
end = datetime(2020, 3, 31)

#iex data source
df = web.DataReader('F', 'iex', start, end)

#https://fred.stlouisfed.org/
#federal reserve bank of St Louis
#many different indices, follow menu and get codes from url.
#https://fred.stlouisfed.org/categories/32255

#https://fred.stlouisfed.org/series/GS10
#10-Year Treasury Constant Maturity Rate (GS10)
df = pdr.get_data_fred('GS10', start, end)
#pandas_datareader.get_data_fred
df = pdr.get_data_fred('BAMLHYH0A0HYM2TRIV', start, end)
#https://fred.stlouisfed.org/series/BAMLHYH0A0HYM2TRIV
df = pdr.get_data_fred('SP500', start, end)

#https://pandas-datareader.readthedocs.io/en/latest/remote_data.html#econdb
df = pdr.DataReader('ticker=RGDPUS', 'econdb')
#https://www.econdb.com/tree/
df = pdr.DataReader('ticker=RBA_C04', 'econdb')#empty result
df = pdr.DataReader('ticker=RBA_C04', 'econdb', start, end)#empty result



RGDPUS




import plotly.plotly as py
The plotly.plotly module is deprecated,
please install the chart-studio package and use the
chart_studio.plotly module instead



from plotly.tools import FigureFactory as FF
from datetime import datetime

fig = FF.create_candlestick(df.Open, df.High, df.Low, df.Close, dates=df.index)
py.iplot(fig, filename='temp', validate=False)



#---------------------old
import plotly.plotly as py
from plotly.tools import FigureFactory as FF
from datetime import datetime

import pandas.io.data as web
from pandas_datareader import data, wb

df = web.DataReader("aapl", 'yahoo', datetime(2007, 10, 1), datetime(2009, 4, 1))
fig = FF.create_candlestick(df.Open, df.High, df.Low, df.Close, dates=df.index)
py.iplot(fig, filename='finance/aapl-candlestick', validate=False)
