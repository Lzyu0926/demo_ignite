from ast import And
from pyignite import Client
import random
client = Client()
client.connect('127.0.0.1', 10800)


#****新增確診者****************************************#
name = input("通報確診者姓名 : ")
account = input("通報確診者帳號(手機號碼) : ")
date = input("通報時間: ")

if( len(str(name))!=0 and len(str(date))==9 and len(str(account))==10 ) :
    r = random.randint(0, 100000000)
    CONFIRMED_INSERT_QUERY = "INSERT INTO Confirmed(Name, ID, Date, key) VALUES ("
    CONFIRMED_INSERT_QUERY += "\'" + name + "\', "
    CONFIRMED_INSERT_QUERY += "\'" + account + "\', "
    CONFIRMED_INSERT_QUERY += "\'" + date + "\', "
    CONFIRMED_INSERT_QUERY += "\'" + str(r) + "\')"
    client.sql(CONFIRMED_INSERT_QUERY)
    print("輸入成功!")
else :
    print("格式不符!")

"""
#***印出所有確診與足跡****************#
CONFIRMED_SELECT_QUERY = "SELECT * FROM Confirmed"
confirmeds = client.sql(CONFIRMED_SELECT_QUERY)
for confirmed in confirmeds:
    print(*confirmed)

#******************************************************#
FOOTPRINT_SELECT_QUERY = "SELECT * FROM Footprint"

footprints = client.sql(FOOTPRINT_SELECT_QUERY)
for footprint in footprints:
    print(*footprint)

"""
