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
URL='https://exchange.sundaeswap.finance/#/'
SCRAPPED_PATH_BASE_FOLDER = 'D:\ICARO\Proyectos\SeleniumSundaeSwap\Scrapped'
SCRAPPED_PATH_BASE_FILENAME = 'sundaeswap_scrapped_'
SCROLL_PAUSE_TIME = 0.5
SAVE_TO_CSV = True
GET_TOKENS = int(70)
XPATH_BASE = '//*[@id="root"]/div[1]/main/div[2]/div[2]/div/div[1]/div[1 <= position() and position() < ' + str(GET_TOKENS) + ']'
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

# pairDivs = driver.find_elements_by_xpath('//*[@id="root"]/div[1]/main/div[2]/div[2]/div/div[1]/div[1 <= position() and position() < 100]')
# pairDivs = driver.find_elements_by_xpath(XPATH_BASE)
# print('pairDivs', len(pairDivs))

listPairs = list()
listLPFee = list()
listPrices = list()
listTAssetL = list()
listTAdaL = list()
listTAdaV24 = list()

divPairNames = driver.find_elements_by_xpath(XPATH_BASE+'/div/div[1]/div/span/span')
print('divPairNames', len(divPairNames))
divPairLPFees = driver.find_elements_by_xpath(XPATH_BASE+'/div/div[1]/div/span/div/div[1]/div')
print('divPairLPFees', len(divPairLPFees))
divPrices = driver.find_elements_by_xpath(XPATH_BASE+'/div/div[2]/div')
print('divPrices', len(divPrices))
divTotalAssetLockeds = driver.find_elements_by_xpath(XPATH_BASE+'/div/div[3]/div')
print('divTotalAssetLockeds', len(divTotalAssetLockeds))
divTotalAdatLockeds = driver.find_elements_by_xpath(XPATH_BASE+'/div/div[4]/div')
print('divTotalAdatLockeds', len(divTotalAdatLockeds))
divTotalAdaVols = driver.find_elements_by_xpath(XPATH_BASE+'/div/div[5]/div')
print('divTotalAdaVols', len(divTotalAdaVols))

for i in range(GET_TOKENS):
# for i in range(10):
    try:
        # print(i, divPairNames[i].text.replace('\n',''))
        # print(i, divPairLPFees[i].text.replace('\n',''))
        # print(i, divPrices[i].text.replace('\n',''))
        # print(i, divTotalAssetLockeds[i].text.replace('\n',''))
        # print(i, divTotalAdatLockeds[i].text.replace('\n',''))
        # print(i, divTotalAdaVols[i].text.replace('\n',''))
        listPairs.append(divPairNames[i].text.replace('\n',''))
        listLPFee.append(divPairLPFees[i].text.replace('\n','').replace('%LP Fee',''))
        listPrices.append(divPrices[i].text.replace('\n','').replace(' ₳',''))
        listTAssetL.append(divTotalAssetLockeds[i].text.replace('\n',''))
        listTAdaL.append(divTotalAdatLockeds[i].text.replace('\n',''))
        listTAdaV24.append(divTotalAdaVols[i].text.replace('\n','').replace(' ₳',''))
    except:
        print('ERROR AT:', i)

driver.close()

# %%
now = datetime.now()
datenow = date.today()
timenow = datetime.now().strftime("%H:%M:%S")
dayminute = datetime.now().hour * 60 + datetime.now().minute
df = pd.DataFrame({'Pair': listPairs,
     'LpFee': listLPFee,
     'PairPrice': listPrices,
     'TotalAssetLocked': listTAssetL,
     'TotalAdaLocked': listTAdaL,
     'AdaVolume24hs': listTAdaV24,
     'DateTime': now,
     'Date': datenow,
     'Time': timenow,
     'MinuteOfDay': dayminute
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


