from ast import And
from pyignite import Client
import random
client = Client()
client.connect('127.0.0.1', 10800)

import time
import os, sys

# Accounts management
def manager_footprints():
    now = time.localtime()
    nowTime = "此系統提供查詢截至 " + time.strftime("%Y-%m-%d, %H:%M:%S", now) + " 之足跡資料"
    print(nowTime)

    FOOTPRINT_SELECT_QUERY = "SELECT Name, ID, Date , Place FROM Footprint"
    footprints = client.sql(FOOTPRINT_SELECT_QUERY)

    print("\n序號: 註冊名 / 電話 / 足跡紀錄時間 / 地點\n",end="\n")
    count = 1
    for row in footprints:
        print(count ,end=": ")
        print(*row)
        count += 1  