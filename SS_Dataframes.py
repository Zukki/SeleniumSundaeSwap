# %%
import pandas as pd
import numpy as np
import time
from datetime import date, datetime
import calendar
import os


# %% [markdown]
# # DEFINE GLOBAL VARIABLES

# %%
SAVE_CALCULATED_DF = True
SAVE_CALCULATED_DF_PATH_BASE_FOLDER = 'D:\ICARO\Proyectos\SeleniumSundaeSwap\Calculated'
SAVE_CALCULATED_DF_PATH_BASE_FILENAME = 'sundaeswap_calculated.csv'
SAVE_CALCULATED_SMALL_DF_PATH_BASE_FILENAME = 'sundaeswap_calculated_small.csv'
SCRAPPED_FOLDER_PATH = 'D:\ICARO\Proyectos\SeleniumSundaeSwap\Scrapped'
SCRAPPED_BASE_FILENAME = 'sundaeswap_scrapped_'
SCRAPPED_ASSET_LIST_FILE = 'sundaeswap_asset_list.csv'


# %% [markdown]
# # GENERATE DATAFRAME

# %% [markdown]
# ## LOAD ASSET LIST

# %%
dfAssetList = pd.read_csv(SCRAPPED_FOLDER_PATH+'\\'+SCRAPPED_ASSET_LIST_FILE)
dfAssetList.head(3)

# %% [markdown]
# ## LOAD SCRAPPED FILES

# %%
files = os.listdir(SCRAPPED_FOLDER_PATH)
# list(files)

df = pd.DataFrame()

for file in files:
    if file.__contains__(SCRAPPED_BASE_FILENAME):
        try:
            # print('Found:', file)
            dfFound = pd.read_csv(SCRAPPED_FOLDER_PATH+'\\'+file, parse_dates=True, decimal='.')
            df = df.append(dfFound, ignore_index=True)
        except:
            print('Error loading:', file)

print('Dataframe loaded')


# %%
df.head(5)

# %%
df.tail(1)

# %% [markdown]
# ## CONVERT AND CALCULATE

# %% [markdown]
# ### Convert DateTime column

# %%
df['DateTime'] = pd.to_datetime(df['DateTime'])
df.info()

# %%
# d = date(2011, 1, 1)
# print(type(d))
# print(d.timetuple())
# unixtime = time.mktime(d.timetuple())
# unixtime

def getUnixDatetime(datetime: datetime):
    unixtime = time.mktime(datetime.timetuple())
    return '{:.0f}'.format(unixtime)

df['DateTimeUnix'] = df['DateTime'].apply(getUnixDatetime)
# https://www.unixtimestamp.com/

# %%
def stringToFloat(strValue):
    if (type(strValue) == float):
        # print(f'Already float {strValue}')
        return strValue
    else:
        if (strValue == '0'):
            print('found 0')
            return float(0)
        try:
            newVal = strValue.replace(',','')
            return float(newVal)
        except:
            # print(f'Error stringToFloat for {strValue}, returning 0')
            return float(0)
    
df['TotalAssetLocked'] = df['TotalAssetLocked'].fillna(0)
df['TotalAdaLocked'] = df['TotalAdaLocked'].fillna(0)
df['AdaVolume24hs'] = df['AdaVolume24hs'].fillna(0)

df['TotalAssetLocked'] = df['TotalAssetLocked'].apply(stringToFloat)
df['TotalAdaLocked'] = df['TotalAdaLocked'].apply(stringToFloat)
df['AdaVolume24hs'] = df['AdaVolume24hs'].apply(stringToFloat)

# %%
df.info()

# %% [markdown]
# ### Calculate unique pair lp id

# %%
unique = df["Pair"] + '_'+ df["LpFee"].astype(str)
df['_PAIR_ID'] = unique
# df['_PAIR_ID'].unique()

# %% [markdown]
# ### Calculate deltas

# %%
# FILTER_PAIR = 'MIN/ADA'
# FILTER_PAIR_LP_FEE = 0.3
# FILTER_PAIR_ID = FILTER_PAIR + '_'+ str(FILTER_PAIR_LP_FEE)
# filterAsset = df['_PAIR_ID'] == FILTER_PAIR_ID
# # from numpy_ext import rolling_apply
# def tryDelta(dfd: pd.DataFrame):
#     #diffs_a = pd.rolling_apply(dfd['PairPrice'], 2, lambda x: x[0] - x[1])
#     print(dfd.rolling(1)['PairPrice'])
    

# tryDelta(df[filterAsset])

# %%
# dif = df[filterAsset].groupby('_PAIR_ID')['PairPrice'].diff()
df['_DELTA_PAIRPRICE'] = df.groupby('_PAIR_ID')['PairPrice'].diff()
df['_DELTA_TOTALASSETLOCKED'] = df.groupby('_PAIR_ID')['TotalAssetLocked'].diff()
df['_DELTA_TOTALADALOCKED'] = df.groupby('_PAIR_ID')['TotalAdaLocked'].diff()

df['_DELTA_DATETIME_SECONDS'] = df.groupby('_PAIR_ID')['DateTime'].diff().dt.seconds
df['_DELTA_DATETIME_MINUTES'] = df.groupby('_PAIR_ID')['DateTime'].diff().dt.seconds/60

# %% [markdown]
# ## GENERATE SMALL VERSION

# %%
dfsmall = df.copy()
dfsmall.drop(axis=1, columns= ['Date','Time','MinuteOfDay','LpFee','Pair','DateTime','_DELTA_DATETIME_MINUTES'], inplace=True)
dfsmall.tail(1)

# %% [markdown]
# # SAVE CALCULATED DF

# %%
if SAVE_CALCULATED_DF:
    # dt_string = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")

    filename= SAVE_CALCULATED_DF_PATH_BASE_FOLDER + '\\' + SAVE_CALCULATED_DF_PATH_BASE_FILENAME
    print(filename)
    df.to_csv(filename, index=False)
    print('Saved', datetime.now())
    
    filename= SAVE_CALCULATED_DF_PATH_BASE_FOLDER + '\\' + SAVE_CALCULATED_SMALL_DF_PATH_BASE_FILENAME
    print(filename)
    dfsmall.to_csv(filename, index=False)
    print('Saved small', datetime.now())


