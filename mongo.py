import requests
import pymongo
import datetime
json_data = requests.get(
    "https://data.moa.gov.tw/Service/OpenData/FromM/PoultryTransGooseDailyPriceData.aspx?IsTransData=1&UnitId=059"
).json()
# Firewall only allow /32
client = pymongo.MongoClient("mongodb://34.121.85.42:27017/")
time = datetime.datetime.strptime(json_data[0]["日期"], "%Y/%m/%d")
client.get_database("price").get_collection("goose_price").insert_one(
    {"timeField": time ,**json_data[0]}
)
