from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

# function to take care of downloading file
def enable_download_headless(browser,download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)

# instantiate a chrome options object so you can set the size and headless preference
# some of these chrome options might be uncessary but I just used a boilerplate
# change the <path_to_download_default_directory> to whatever your default download folder is located
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')
chrome_options.add_experimental_option("prefs", {
        "download.default_directory": "<path_to_download_default_directory>",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
})
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')

# initialize driver object and change the <path_to_chrome_driver> depending on your directory where your chromedriver should be
chrome_driver_path = "D:/2020/coding/stock_analysis/chrome_drivers/chromedriver.exe"
#driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver_path)
#DeprecationWarning: use options instead of chrome_options
driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver_path)

# change the <path_to_place_downloaded_file> to your directory where you would like to place the downloaded file
download_dir = "asx_announcements"

# function to handle setting up headless download
enable_download_headless(driver, download_dir)

# get request to target the site selenium is active on
driver.get("https://www.thinkbroadband.com/download")

# initialize an object to the location on the html page and click on it to download
search_input = driver.find_element_by_css_selector('#main-col > div > div > div:nth-child(8) > p:nth-child(1) > a > img')
search_input.click()
