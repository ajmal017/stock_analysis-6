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


#import requests #imported at top
rowpos=1

row = rows[1]
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
new_url = xpath.get_attribute("href")
print("href = ", new_url)#this is downloadable link.
# Save the window opener (current window, do not mistaken with tab... not the same)
main_window = browser.current_window_handle
#
browser2 = webdriver.Chrome(chromedriver)
browser2.get(new_url)
agree_proceed_button = browser2.find_element_by_xpath('/html/body/div/form/input[2]')
agree_proceed_button
agree_proceed_button.click()
current_url = browser2.current_url
print(current_url)
import requests
r = requests.get(current_url, allow_redirects=True)
open("asx_announcements/"+stock_code+"_"+str(rowpos)+"_"+'.pdf', 'wb').write(r.content)
#https://gist.github.com/lrhache/7686903
from selenium.webdriver.common.keys import Keys
# Close current tab
browser2.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
# Put focus on current window which will be the window opener
browser.switch_to_window(main_window)
