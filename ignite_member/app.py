from cmath import e
import email
from matplotlib.collections import Collection
import certifi
from pyignite import Client
from flask import *

client = Client()
client.connect('127.0.0.1', 10800)
print("資料庫連線成功")

app = Flask(
    __name__,
    static_folder="static",  #控制 static 的位置
    static_url_path="/"
)
app.secret_key = "abchahaha"


@app.route("/")
def homepage():
    msg = request.args.get("msg","")
    if msg == "success":
        return render_template("homepage.html",msg="註冊成功")
    else:
        return render_template("homepage.html")
    

@app.route("/signin",methods = ["POST"])
def signin():

    #前端接收資料
    phone = request.form["phone"]
    password= request.form["password"]

    #根據資料與資料庫互動
    # ACCOUNT_SELECT_QUERY = "SELECT * FROM Account WHERE ID ='" + phone + "' AND password = " + "'"+password +"'"
    ACCOUNT_SELECT_QUERY = "SELECT * FROM Account WHERE ID ='" + phone +"'"
    accounts = client.sql(ACCOUNT_SELECT_QUERY)
    
    
    # 判斷電話號碼資料庫裡有沒有
    # 有 -> 密碼錯誤 -> 再輸入一次
    # 有 -> 密碼正確 -> 導入會員頁面(memberpage) -> 印出接觸史
    #沒有-> 註冊頁面註冊(signin) -> 成功 -> 導回登入頁面(homepage)
    #(問題：為什麼輸入太短會error)

    ###############       有問題       ###################
    count = 0
    for row in accounts:
        count=count+1
    if count == 0 :
        return render_template("signuppage.html",msg="請輸入電話及密碼")  
    else :
        ACCOUNT_SELECT_QUERY = "SELECT * FROM Account WHERE ID ='" + phone + "' AND password = " + "'"+password +"'"
        ac = client.sql(ACCOUNT_SELECT_QUERY)
        cnt = 0
        for row in ac:
            cnt=cnt+1
        if cnt == 0 :
            return render_template("homepage.html",msg="密碼輸入錯誤")  
        else:
            session["phone"] = phone
            return render_template("memberpage.html")  
    #####################################################

    # return redirect("/?msg=success")

@app.route("/signup",methods=["POST"])
def signup():
    return render_template("signuppage.html")  
    
@app.route("/signuppage",methods=["POST"])
def signuppage():
    name = request.form["name"]
    phone = request.form["phone"]
    password = request.form["password"]
    password_2 = request.form["password_2"]
    

    #註冊
    #輸入電話及密碼、確認密碼(不得與其他手機號碼重複)
    #確認後將資料輸入到SQL（怎麼插入）
    #導回首頁(homepage)，印出註冊成功

    ###############       怎麼插       ###################
    
    ACCOUNT_SELECT_QUERY = "SELECT * FROM Account WHERE ID ='" + phone +"'"
    accounts = client.sql(ACCOUNT_SELECT_QUERY)

    count = 0 #如果accounts篩出來是空的 count就會是0 檢測是否有註冊

    for row in accounts:
        count=count+1

    if count == 0 :
        if password != password_2:
            return render_template("signuppage.html",msg="兩次密碼不符")
        ACCOUNT_INSERT_QUERY = '''INSERT INTO Account(
            Name, ID, Password, Date , Place
        ) VALUES (?, ?, ?, ?,?)'''

        ACCOUNT_DATA = [
            [name,phone,password, '#','#']
        ]

        for row in ACCOUNT_DATA:
            client.sql(ACCOUNT_INSERT_QUERY, query_args=row)
        return render_template("homepage.html",msg="註冊成功")
    else :
        return render_template("homepage.html",msg="手機已被註冊")

    #####################################################


@app.route("/signout")
def signout():
    #登出
    del session["nickname"]
    return redirect("/")


@app.route("/member") 
def memberpage():
    #有接觸史 -> 印出接觸的日期、時間、地點等等
    #無接觸史 
    #要有一個登出按鈕 -> 導回首頁

    if "phone" in session:
        return render_template("memberpage.html") 
    else:
        return redirect("/")

@app.route("/connectsearch",methods=["POST"])
def connectsearch():
    phone = session["phone"]
    return render_template("connectpage.html",msg=phone)  

@app.route("/connectsearchpage",methods=["POST"])
def connectsearchpage():
    ##將帳號密碼對應帳號的 Name 日期 地點 匯入
    phone = session["phone"]
    FOOTPRINT_SELECT_QUERY = "SELECT Name,Date,Place FROM Footprint WHERE ID = '" + phone +"'"
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
    return render_template("connectpage.html",msg=phone) 


@app.route("/diagnosed",methods=["POST"])
def diagnosed():
    return render_template("diagnosedpage.html")


#/error?msg=錯誤訊息
@app.route("/error")
def error():
    msg = request.args.get("msg","發生錯誤")
    return render_template("errorpage.html", msg=msg) #傳入錯誤msg



app.run() #這要放最後面