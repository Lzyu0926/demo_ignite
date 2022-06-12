# demo_ignite

這是一份能實踐由民眾、政府、醫療機構三方，共同聯繫的實聯制與確診足跡比對系統

&nbsp;

## Ignite 前置作業

### 開啟一個終端機執行 `ignite` 

透過 `bin/ignite.sh` (Mac作業環境) 或 `bin/ignite.bat` (Windows10後作業環境)

( 在有需要時執行 `../examples/config/example-ignite.xml` ) // 待確定

&nbsp;

## Python 前置作業

此程式需要 `flask` 與 `pyignite`

若未安裝請透過

`pip install flask`

`pip install pyignite`

&nbsp;

## 系統初始化

### 請透過 `python Server.py` 初始化並啟動平台

&nbsp;

## 三方存取介面

### 民眾端

進入 `/ignite_member` 資料夾並透過 `python app.py` 取得 Html 客戶端網頁連結

`http://127.0.0.1:5000`

即可透過網頁內文字引導與網頁回饋來執行

1. 註冊手機並登錄獲取服務
2. 在有接觸到資料庫內確診者的情況下，顯示最近一次(時間戳記最大)的接觸史資料
3. 登入自己的足跡實聯制資料(包含輸入姓名驗證、時間與地點)

### 政府端

進入 `/ignite_cdc` 資料夾並透過 `main.py` 執行以下三種顯示資料功能

1. 查詢已經註冊的手機資訊
2. 查詢已經輸入的足跡資訊
3. 查詢已經被醫療機構通報的確診者資訊

此系統需要透過輸入驗證碼 `0000` 來驗證身分並進入系統 >> 已刪除!!

##### 未來功能 新增能夠透過中央刪除一定時間前之足跡與確診者資料

### 醫療機構端

透過 `Cases_Report.py` 來新增確診者

(輸入非空白之姓名、符合格式之電話號碼 與 9碼日期資訊 Ex. `2099_0909`、`yyyy_mmdd`)
