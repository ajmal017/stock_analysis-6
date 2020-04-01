


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
browser.quit()
