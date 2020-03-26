import datetime
import yfinance as yf
msft = yf.Ticker("CBA.AX")
msft = yf.Ticker("^KS11")
msft = yf.Ticker("^HSI")
msft = yf.Ticker("^BSESN")
msft = yf.Ticker("^KOSDAQ")
# get stock info
print(msft.info)
print(msft.info.keys())
for key in msft.info.keys():
    print (key, msft.info[key])

msft.info['longName']
msft.info['open']
msft.info['previousClose']
msft.info['lastMarket']
msft.info['volume24Hr']
msft.info['navPrice']
msft.info['bookValue']


msft.history(period="max")
msft.history(start = '2020-01-01', end = '2020-02-02')
#https://github.com/ranaroussi/yfinance/blob/master/yfinance/base.py

result = msft.history(start = '2020-03-23', end = '2020-03-24', interval="5m")

#NB: if start & end time is outside ASX operating hours
#get 'No data found for this date range, symbol may be delisted'
# first time = 10:00:00+11:00
# last time  = 15:55:00+11:00
start = datetime.datetime(2020, 3, 23, 8, 0)
end   = datetime.datetime(2020, 3, 23, 22, 10)
result = msft.history(start = start, end = end, interval="5m")

"""
list(result.columns)
['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
"""

type(result) #dataframe
result.shape

"""
zip
sector
fullTimeEmployees
longBusinessSummary
city
phone
state
country
companyOfficers
website
maxAge
address1
fax
industry
previousClose
regularMarketOpen
twoHundredDayAverage
trailingAnnualDividendYield
payoutRatio
volume24Hr
regularMarketDayHigh
navPrice
averageDailyVolume10Day
totalAssets
regularMarketPreviousClose
fiftyDayAverage
trailingAnnualDividendRate
open
toCurrency
averageVolume10days
expireDate
yield
algorithm
dividendRate
exDividendDate
beta
circulatingSupply
startDate
regularMarketDayLow
priceHint
currency
trailingPE
regularMarketVolume
lastMarket
maxSupply
openInterest
marketCap
volumeAllCurrencies
strikePrice
averageVolume
priceToSalesTrailing12Months
dayLow
ask
ytdReturn
askSize
volume
fiftyTwoWeekHigh
forwardPE
fromCurrency
fiveYearAvgDividendYield
fiftyTwoWeekLow
bid
tradeable
dividendYield
bidSize
dayHigh
exchange
shortName
longName
exchangeTimezoneName
exchangeTimezoneShortName
isEsgPopulated
gmtOffSetMilliseconds
quoteType
symbol
messageBoardId
market
annualHoldingsTurnover
enterpriseToRevenue
beta3Year
profitMargins
enterpriseToEbitda
52WeekChange
morningStarRiskRating
forwardEps
revenueQuarterlyGrowth
sharesOutstanding
fundInceptionDate
annualReportExpenseRatio
bookValue
sharesShort
sharesPercentSharesOut
fundFamily
lastFiscalYearEnd
heldPercentInstitutions
netIncomeToCommon
trailingEps
lastDividendValue
SandP52WeekChange
priceToBook
heldPercentInsiders
nextFiscalYearEnd
mostRecentQuarter
shortRatio
sharesShortPreviousMonthDate
floatShares
enterpriseValue
threeYearAverageReturn
lastSplitDate
lastSplitFactor
legalType
morningStarOverallRating
earningsQuarterlyGrowth
dateShortInterest
pegRatio
lastCapGain
shortPercentOfFloat
sharesShortPriorMonth
category
fiveYearAverageReturn
regularMarketPrice
logo_url
"""
