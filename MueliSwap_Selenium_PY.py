# %%
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from datetime import date, datetime

# %%
URL='https://ada.muesliswap.com/markets/featured'
SCRAPPED_PATH_BASE_FOLDER = 'D:\ICARO\Proyectos\SeleniumSundaeSwap\Scrapped'
SCRAPPED_PATH_BASE_FILENAME = 'muesliswap_scrapped_'
SCROLL_PAUSE_TIME = 0.5
SAVE_TO_CSV = True
GET_TOKENS = int(70)
XPATH_BASE = '//*[@id="root"]/div[1]/div/div[2]/div[2]/div[4]/a[1 <= position() and position() < ' + str(GET_TOKENS) + ']'
print('GLOBAL VARIABLES')
print('SAVE_TO_CSV:', SAVE_TO_CSV)
print('GET_TOKENS:', GET_TOKENS)
print('XPATH_BASE:', XPATH_BASE)
print('--------------------------------------------------')

# %%
##############################################################################################################################
### GET WEBSITE
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("start-maximized")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

# from pyvirtualdisplay import Display
# display = Display(visible=0, size=(1920, 1080))
# display.start()

# driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(URL)
time.sleep(6)
print('GET AFTER SLEEP')

# driver.maximize_window()
# print('MAXIMIZE...')
# time.sleep(3)



# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # print('SCROLLING')
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    
print('FINISH SCROLLING')

time.sleep(10)
print('WAITED FOR VALUES TO LOAD')

##############################################################################################################################
### GET DATA

listAssets = list()
listPrices = list()
listChanges = list()
listChangeTypes = list()
listVolumes = list()
listMarketCaps = list()
# //*[@id="root"]/div[1]/div/div[2]/div[2]/div[4]/a[1]

divAssetNames = driver.find_elements_by_xpath(XPATH_BASE+'/div/div[1]/div[2]')
print('divAssetNames', len(divAssetNames))
divPrices = driver.find_elements_by_xpath(XPATH_BASE+'/div/div[2]')
print('divPrices', len(divPrices))
change24s = driver.find_elements_by_xpath(XPATH_BASE+'/div/div[3]/div')
print('change24s', len(change24s))
volume24s = driver.find_elements_by_xpath(XPATH_BASE+'/div/div[4]')
print('volume24s', len(volume24s))
marketCaps = driver.find_elements_by_xpath(XPATH_BASE+'/div/div[5]')
print('marketCaps', len(marketCaps))

for i in range(GET_TOKENS):
# for i in range(10):
    try:
        listAssets.append(divAssetNames[i].text.replace('\n',''))
        listPrices.append(divPrices[i].text.replace('\n','').replace(' ₳',''))
        listChanges.append(change24s[i].text.replace('\n','').replace('%','').replace('↑','').replace('↓',''))
        if '↑' in change24s[i].text:
            listChangeTypes.append('+')
        if '↓' in change24s[i].text:
            listChangeTypes.append('-')
        if '-' in change24s[i].text:
            listChangeTypes.append('=')
        listVolumes.append(volume24s[i].text.replace('\n','').replace(' ₳',''))
        listMarketCaps.append(marketCaps[i].text.replace('\n','').replace(' ₳',''))
    except:
        print('ERROR AT:', i)

driver.close()

# %%
now = datetime.now()

df = pd.DataFrame(
    {'Pair': listAssets,
     'PairPrice': listPrices,
     'Change24hs': listChanges,
     'ChangeType': listChangeTypes,
     'AdaVolume24hs': listVolumes,
     'MarketCapAda': listMarketCaps,
     'DateTime': now
    })

# %%
df.head(10)

# %%
df.tail(3)

# %%
if SAVE_TO_CSV:
    dt_string = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")

    filename= SCRAPPED_PATH_BASE_FOLDER + '\\' + SCRAPPED_PATH_BASE_FILENAME+dt_string+'.csv'
    print(filename)
    df.to_csv(filename, index=False)
    print('Saved')

# %%
# dfindex = df[['Pair','LpFee']]
# dfindex = dfindex.sort_values(by=['Pair','LpFee'])
# dfindex
# dfindex.to_csv('Scrapped\sundaeswap_asset_list.csv', index=False)


