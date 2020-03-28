NB: need to run in windows now ubuntu unless on a machine with headless chrome installed.
https://selenium-python.readthedocs.io/getting-started.html
https://pypi.org/project/selenium/
https://sites.google.com/a/chromium.org/chromedriver/downloads
check chrome > settings > help for version. mine is ver 79.xxx

#nb: use windows cmd prompt not ubuntu bash due to chrome driver config issues.
cd D:\2020\coding\stock_analysis
d:
$python --version
#Python 3.7.7
python -m pip install --upgrade pip

https://programwithus.com/learn-to-code/Pip-and-virtualenv-on-Windows/
pip install virtualenv
virtualenv win_env

#activate the virtual env
win_env\Scripts\activate.bat


pip install selenium

https://pythonspot.com/category/selenium/
----------------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
#options.binary_location = "/usr/bin/chromium"
driver = webdriver.Chrome(executable_path='D:/2020/coding/stock_analysis/chrome_drivers/chromedriver.exe')
#driver = webdriver.Chrome(chrome_options=options)
driver.get('https://www.asx.com.au/asx/markets/optionPrices.do')

element = driver.find_element_by_xpath('/html/body/section[3]/article/div[2]/div/form[1]/input[2]')
element.click()
element.sendKeys("BHP");
----------------------------------

pip install lxml
pip install pandas
#
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions # available since 2.26.0
from selenium.webdriver.support import expected_conditions # available since 2.26.0
from selenium.webdriver.common.by import By
import pandas as pd
chromedriver = "D:/2020/coding/stock_analysis/chrome_drivers/chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)
browser.get('https://www.asx.com.au/asx/markets/optionPrices.do')
#use chrome > inspect > copy element to get html.
#<input id="underlyingCode" name="underlyingCode" type="text" value="" size="6" maxlength="6">
formElem = browser.find_element_by_id('underlyingCode')
formElem.send_keys("BHP")
#<input id="submit" class="actionbutton" value="Go" type="submit" onclick="trackAsxCode()">
submitButton = browser.find_element_by_id('submit')
submitButton.click()
#this retrieves table of options on the stock.

#
colnames = ['code', 'expiry_date', 'put_call', 'exercise', 'bin', 'offer', 'last', 'volume', 'open_interest', 'margin_price']
df = pd.DataFrame(columns=colnames)

optionsTableElement = browser.find_element_by_id('optionstable')
type(optionsTableElement)
#<tr class="altrow showzeroopeninterest">
#rows = optionsTableElement.find_elements_by_class_name('showzeroopeninterest')
#nbb: sometimes uses class  "altrow ", "altrow showzeroopeninterest" or just " showzeroopeninterest"
#<tr class="altrow ">
rows = optionsTableElement.find_elements_by_tag_name('tr')


type(rows)
len(rows)#1518 rows

for row in rows[1:]:
    print(row)
    row_values = []
    cells_stockcode = row.find_elements_by_tag_name("th")[0].text
    row_values.append(cells_stockcode)
    print("cells_stockcode:", cells_stockcode)
    cells = row.find_elements_by_tag_name("td")
    print(type(cells), len(cells))
    for cell in cells:
        print(cell.text)
        row_values.append(cell.text)
    print("row_values:", row_values)
    a_series = pd.Series(row_values, index = df.columns)
    df = df.append(a_series, ignore_index=True)
    print("df.shape:", df.shape)
    #break
file_out_prefix = "BHP_options_27-3-2020"#dynamically construct this w stock code and date of run
compression_opts = dict(method='zip', archive_name=file_out_prefix+'.csv')
df.to_csv('data_collected/"+file_out_prefix+".zip', index=False, compression=compression_opts)


#this almost works but errors when missing data. needs to use tr and td
table_text = optionsTableElement.text
table_text_lines = table_text.splitlines()
len(table_text_lines)
#1520 vs 691 rows above.
#when copy paste from web page get 1518 rows including col names
#due to html making multiple rows for column header/names display.
count=0
for text in table_text.splitlines():
    #print (text)
    row_values = []
    count = count+1
    if count>3:
        for tab_text in text.split(" "):
            row_values.append(tab_text)
        print(row_values)
        a_series = pd.Series(row_values, index = df.columns)
        df = df.append(a_series, ignore_index=True)
        print("df.shape:", df.shape)








#-------------------------------------------------------------------------------
# could not get selenium to work on ubuntu

https://blog.testproject.io/2018/02/20/chrome-headless-selenium-python-linux-servers/
install xvfb (fake X server)

https://zoomadmin.com/HowToInstall/UbuntuPackage/xvfb
sudo apt-get update -y
sudo apt-get install -y xvfb

pip install PyVirtualDisplay

env | grep DISPLAY
#should be 1


https://linuxize.com/post/how-to-install-google-chrome-web-browser-on-ubuntu-18-04/

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#to start
google-chrome
chromium-browser

google-chrome www.google.com
google-chrome --help

# could not get selenium to work on ubuntu
#-------------------------------------------------------------------------------
