'''
windows dos prompt
cd D:\2020\coding\stock_analysis
d:
#activate virtual environment
win_env\Scripts\activate.bat
python

https://pypi.org/project/requests/
pip install requests
'''
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import requests
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")

chromedriver = "D:/2020/coding/stock_analysis/chrome_drivers/chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)


stock_code = "CBA"
browser.get('https://www.asx.com.au/asx/statistics/announcements.do')
#<input id="issuerCode" name="asxCode" type="text" value="" size="8" maxlength="3">
element = browser.find_element_by_id('issuerCode')
element.click()
element.send_keys(stock_code);
#dropdown element
ddelement = Select(browser.find_element_by_name('period'))
#ddelement.select_by_index(1)
ddelement.select_by_visible_text('The past week')
#<input type="submit" value="Search" class="actionbutton">
element = browser.find_element_by_class_name('actionbutton')
element.click()
#load page
#find table
#//*[@id="content"]/div/announcement_data
element = browser.find_element_by_tag_name('announcement_data')
table_element = browser.find_element_by_tag_name('table')
rows = table_element.find_elements_by_tag_name('tr')

'''
ASX rules
https://www.asx.com.au/documents/rules/gn14_asx_market_announcements_platform.pdf
summary by morningstar
https://datanalysis.morningstar.com.au/licensee/datpremium/html/ASX_Announcements_Onesheet.pdf


Becoming a substantial holder
Ceasing to be a substantial holder
Change in substantial holding
Trading Halt
Notice of Annual General Meeting
Results of Annual General Meeting

#unoffical
Pause in Trading
ratings update
COVID-19

'''

#import requests #imported at top
rowpos=1
for row in rows[rowpos:2]:
    print("rowpos:", rowpos)
    print(row)
    cells = row.find_elements_by_tag_name("td")
    i=0
    for cell in cells:
        print("i="+str(i), cell.text+"\n_______________")
        a_elem = cell.find_elements_by_tag_name("a")
        print ("a_elem:", a_elem)
        i += 1
    xpath = cell.find_element_by_xpath('//*[@id="content"]/div/announcement_data/table/tbody/tr['+str(rowpos)+']/td[3]/a')
    print("xpath=a:", xpath)
    print("xpath.text:", xpath.text)
    print("href = ", xpath.get_attribute("href"))#this is downloadable link.
    # Save the window opener (current window, do not mistaken with tab... not the same)
    main_window = browser.current_window_handle
    #
    browser.get(xpath.get_attribute("href"))
    # Open the link in a new tab by sending key strokes on the element
    # Use: Keys.CONTROL + Keys.SHIFT + Keys.RETURN to open tab on top of the stack
    first_link.send_keys(Keys.CONTROL + Keys.RETURN)
    # Switch tab to the new tab, which we will assume is the next one on the right
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
    # Put focus on current window which will, in fact, put focus on the current visible tab
    browser.switch_to_window(main_window)
    # do whatever you have to do on this page, we will just got to sleep for now
    sleep(2)
    # Close current tab
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
    # Put focus on current window which will be the window opener
    browser.switch_to_window(main_window)

#test if this element available > /html/body/div/form/input[2]
agree_process_cell.find_element_by_xpath('/html/body/div/form/input[2]')

    r = requests.get(xpath.get_attribute("href"), allow_redirects=True)
    open("asx_announcements/"+stock_code+"_"+str(rowpos)+"_"+'.pdf', 'wb').write(r.content)

    link = cells[2].get_attribute("href")
    print ("link:", link)
