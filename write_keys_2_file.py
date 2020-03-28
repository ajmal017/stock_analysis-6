import yfinance as yf
msft = yf.Ticker("CBA.AX")

file1 = open("data/yfinance_keys.txt","a")
for key in msft.info.keys():
    print (key)
    file1.write(key+"\n")
file1.close()
