from ast import And
from pyignite import Client
import random
client = Client()
client.connect('127.0.0.1', 10800)

import time
import os, sys

# Accounts management
def manager_ID():
    now = time.localtime()
    nowTime = "此系統提供查詢截至 " + time.strftime("%Y-%m-%d, %H:%M:%S", now) + " 之帳號資料"
    print(nowTime)

    ACCOUNT_SELECT_QUERY = "SELECT Name, ID FROM Account"
    accounts = client.sql(ACCOUNT_SELECT_QUERY)

    print("\n序號: 註冊名 / 電話\n",end="\n")
    count = 1
    for row in accounts:
        print(count ,end=": ")
        print(*row)
        count += 1  