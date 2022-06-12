from manager_Cases import manager_case
from manager_Footprints import manager_footprints
from manager_ID import manager_ID
from pyignite import Client
import os, sys

client = Client()
client.connect('127.0.0.1', 10800)

while(True):
    print("1.查詢註冊帳號\n2.查詢足跡\n3.查詢確診案例\n4.離開")
    choose=input()
    if(choose=='1'):
        manager_ID()
    elif(choose=='2'):
        manager_footprints()
    elif(choose=='3'):
        manager_case()
    else:
        os._exit(0)
    print("-------------------------------\n")