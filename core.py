import requests
import time
import datetime
import pandas as pd
import pathlib
import pdb

URL = "https://api.coinmarketcap.com/v1/ticker/?limit=300"
UNSTORED_UPDATES = 0

path = pathlib.Path("./coinmarketcap.csv")

if path.exists():
    df = pd.read_csv(str(path))
else:
    df = pd.DataFrame()

while True:

    try:
        response = requests.get(URL)
    except:
        print("ERROR")
        response = None

    if response.status_code == 200:
        df = pd.concat([
            df,
            pd.DataFrame(response.json())
        ]).drop_duplicates(["id", "last_updated"])

        try:
            print(
                df.shape,
                df.last_updated.astype(int).max(),
                datetime.datetime.now()
            )
        except:
            pdb.set_trace()

    if UNSTORED_UPDATES >= 10:
        df.to_csv("coinmarketcap.csv", index=False)
        print("STORED DATA TO DISK")
        UNSTORED_UPDATES = 0
    else:
        UNSTORED_UPDATES += 1

    time.sleep(120)

