# A.資料庫
## 1 
* SQL
  * 關聯式資料庫
* NoSQL
  * 非關聯式資料庫
* 主要差異
  * SQL需要完整定義欄位，更動欄位時需要更仔細的migration
  * NoSQL 可以靈活存儲非結構化資料
  * SQL著重在資料操作的準確和一致性
  * SQL在資料分析上可以透過SQL語法，將不同資料表的資料組合呈現
* 運用場景
  * NoSQL 比較適合資料欄位不確定，或是非結構化資料使用(資料之間沒有複雜關聯)
  * SQL 資料之間有複雜關聯，欄位已經定義完整的應用
## 2
* 1NF
  * 一個欄位只能有單一值
  * 消除意義重複欄位
  * 決定主鍵
* 2NF
  * 消除部分相依
* 3NF
  * 消除遞移相依
1. 提昇儲存資料與資料庫操作效率
2. 減少資料異常
3. 使資料庫維護更容易
## 3
詳見 Roar_backend\json2djangoDB.py
# B
> 上面的資料洗太久了，所以B部分我用我有使用過的套件及作法去做
> DRF+Nuxt3做前後端分離
## a
* /operation/api/dj-rest-auth/registration/
  * POST
* /operation/api/dj-rest-auth/login/
  * POST
## b
* /operation/api/show/<int:pk>/
  * Public
    * GET
  * Protect
    * POST
    * DELETE
    * PATCH
    * PUT
## c
見`mongo.py`
我也不知道要抓甚麼比較好，
定時任務我應該會塞給crontab
Celery還沒看懂怎麼用
# c  
http://34.121.85.42/
cloudflare DNS and proxy
https://roar.virgil246.com
http://roar.virgil246.com



# d
