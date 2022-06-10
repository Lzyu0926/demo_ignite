from ast import And
from pyignite import Client
import random
client = Client()
client.connect('127.0.0.1', 10800)

#*註冊*********************************************#
name = input("註冊姓名 : ")
account = input("註冊帳號(手機號碼) : ")
password = input("註冊密碼 : ")

ACCOUNT_SELECT_QUERY = "SELECT * FROM Account WHERE ID ='" + account + "' AND password = " + "'"+password +"'"
accounts = client.sql(ACCOUNT_SELECT_QUERY)

count = 0 #如果accounts篩出來是空的 count就會是0 檢測是否有註冊
for row in accounts:
    count=count+1
if count == 0 :
    print("可以註冊")
    ACCOUNT_INSERT_QUERY = '''INSERT INTO Account(
        Name, ID, Password, Date , Place
    ) VALUES (?, ?, ?, ?,?)'''

    ACCOUNT_DATA = [
        [name,account,password, '#','#']
    ]

    for row in ACCOUNT_DATA:
        client.sql(ACCOUNT_INSERT_QUERY, query_args=row)
else :
    print("已經註冊過了")
#*************************************************#

#**顯示接觸確診者記錄******************************#
yesOrNo = input("是否要查詢有無接觸確診者(Y/N)")

if yesOrNo == 'Y' :
    ##將帳號密碼對應帳號的 Name 日期 地點 匯入
    FOOTPRINT_SELECT_QUERY = "SELECT Name,Date,Place FROM Footprint WHERE ID = '" + account +"'"
    footprints = client.sql(FOOTPRINT_SELECT_QUERY)
    ##將確診者的資料匯入
    CONFIRMED_SELECT_QUERY = "SELECT Name,Date,Place FROM Confirmed"
    confirmeds = client.sql(CONFIRMED_SELECT_QUERY)

    count = 0
    c = 0 
    ##遍歷所有資料
    for row in footprints :
        place = row[2]
        date = row[1]
        ##將確診者與足跡中地點時間相同者的資料匯入
        #(變數) = SELECT 目標欄位 WHERE 條件相符
        CONFIRMED_SELECT_QUERY = "SELECT Name,Date,Place FROM Confirmed WHERE Place = '"+place+"' AND Date = '"+date +"'"
        #一定要加client.sql才會執行 要不然只是字串
        confirmeds = client.sql(CONFIRMED_SELECT_QUERY)
        count = 0
        for r in confirmeds:
            count = count+1
        if count != 0 :
            print("有接觸")
            print(*r)
            c = c+1
    if c == 0 :
        print("無接觸")
#*****************************************************#


#****新增確診者****************************************#
name = input("通報確診者姓名 : ")
account = input("通報確診者帳號(手機號碼) : ")
password = input("通報確診者密碼 : ")
#找出確診者足跡
FOOTPRINT_SELECT_QUERY = "SELECT * FROM Footprint WHERE ID = '" + account +"'"
footprints = client.sql(FOOTPRINT_SELECT_QUERY)

CONFIRMED_INSERT_QUERY = '''INSERT INTO Confirmed(
    Name, ID, Password, Date , Place,key
) VALUES (?, ?, ?, ?,?,?)'''

for row in footprints :
    INSERT_DATA = [[row[0],row[1],row[2],row[3],row[4],random.randint(0, 100000000)]]
    for rows in INSERT_DATA:
        client.sql(CONFIRMED_INSERT_QUERY, query_args=rows)
#***印出所有確診足跡****************#
CONFIRMED_SELECT_QUERY = "SELECT * FROM Confirmed"
confirmeds = client.sql(CONFIRMED_SELECT_QUERY)
for confirmed in confirmeds:
    print(*confirmed)
#******************************************************#

