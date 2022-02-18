# %%
import requests
#from requests.auth import HTTPDigestAuth
import json
import pandas as pd
from datetime import date, datetime

# %%
url = "https://601fa5cgn2.execute-api.us-east-1.amazonaws.com/Dev/assets?asset=SUNDAE/ADA_0.3"
myResponse = requests.get(url)
print (myResponse.status_code)
jData = {}
# For successful API call, response code will be 200 (OK)
if(myResponse.ok):
    jData = json.loads(myResponse.content)
    print("The response contains {0} properties".format(len(jData)))
else:
  # If response code is not ok (200), print the resulting http error code with description
    myResponse.raise_for_status()


# %%
jData[0]

# %%
df = pd.DataFrame(jData, columns =['PairId','Index','DateTimeUnix','PairPrice'])
df = df.set_index('Index')

# %%
df.info()

# %%
def datetimeFromUnix(ts:str):
    return datetime.utcfromtimestamp(int(ts))

df['PairPrice'] = df['PairPrice'].astype(float)
df['DateTime'] = df['DateTimeUnix'].apply(datetimeFromUnix)
df.info()

# %%
df.head(5)


