import json, sqlite3
from pydantic import BaseModel
from datetime import datetime


class Location(BaseModel):
    location: str
    locationName: str
    latitude: str | None
    longitude: str | None


class ShowTime(Location):
    time: str
    endTime: str
    onSales: str | bool
    price: str

    def __init__(self, **data):
        super().__init__(**data)
        self.onSales = True if data["onSales"] == "Y" else False


class showInfo(BaseModel):
    UID: str
    version: str
    title: str
    category: str
    discountInfo: str
    descriptionFilterHtml: str
    imageUrl: str
    webSales: str
    sourceWebPromote: str
    sourceWebName: str
    comment: str
    editModifyDate: str
    hitRate: int
    showInfo: list[ShowTime]
    masterUnit: list[str]
    supportUnit: list[str]
    otherUnit: list[str]
    subUnit: list[str]
    showUnit: str | list[str]

    def __init__(self, **data):
        super().__init__(**data)
        if not self.showUnit:
            self.showUnit = []
        else:
            self.showUnit = self.showUnit.split(";")


with open("SearchShowAction.json", encoding="utf-8") as f:
    j = json.loads(f.read())
con = sqlite3.connect("test.db")
cur = con.cursor()

for i in j:
    a = showInfo(**i)
    cur.execute(
        "INSERT INTO SHOW_INFO VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
        (
            a.UID,
            a.version,
            a.title,
            a.category,
            a.discountInfo,
            a.descriptionFilterHtml,
            a.imageUrl,
            a.webSales,
            a.sourceWebPromote,
            a.comment,
            a.editModifyDate,
            a.hitRate,
        ),
    )
    for unit in a.supportUnit:
        cur.execute("INSERT INTO SUPPORT_UNIT VALUES(?,?)", (unit, a.UID))
    for unit in a.masterUnit:
        cur.execute("INSERT INTO MASTER_UNIT VALUES(?,?)", (unit, a.UID))
    for unit in a.otherUnit:
        cur.execute("INSERT INTO OTHER_UNIT VALUES(?,?)", (unit, a.UID))
    for unit in a.subUnit:
        cur.execute("INSERT INTO SUB_UNIT VALUES(?,?)", (unit, a.UID))
    for unit in a.showUnit:
        cur.execute("INSERT INTO SHOW_UNIT VALUES(?,?)", (unit, a.UID))

    cur.execute("INSERT INTO SOURCE_WEB_NAME VALUES(?,?)", (a.sourceWebName, a.UID))
    for time in a.showInfo:
        cur.execute(
            "SELECT location_id FROM LOCATION WHERE name=?", (time.locationName,)
        )
        row = cur.fetchone()
        if row:
            loaction_ID = row[0]
        else:
            cur.execute(
                """INSERT INTO LOCATION
                        (address,name,lat,lng)
                        VALUES (?,?,?,?)""",
                (time.location, time.locationName, time.latitude, time.longitude),
            )
            loaction_ID = int(cur.lastrowid)
        cur.execute(
            """INSERT INTO SHOW_TIME (
            show_uid,
            location_id,
            time,
            on_sales,
            price,
            end_time)
            VALUES (?,?,?,?,?,?)""",
            (a.UID, loaction_ID, time.time, time.onSales, time.price, time.endTime),
        )
    con.commit()
