import json
import sqlite3
from pydantic import BaseModel, BeforeValidator
from datetime import datetime
from typing_extensions import Annotated
from decimal import Decimal

CustomDateTime = Annotated[
    datetime, BeforeValidator(lambda x: datetime.strptime(x, "%Y/%m/%d %H:%M:%S"))
]


class Location(BaseModel):
    location: str
    locationName: str
    latitude: Decimal | None
    longitude: Decimal | None


class ShowTime(Location):
    time: CustomDateTime
    endTime: CustomDateTime
    onSales: Annotated[bool, BeforeValidator(lambda x: True if x == "Y" else False)]
    price: str


class Unit(BaseModel):
    tag: None | str
    name: str


def unit_unserializer(data):
    import re

    tag = None
    name = None
    re_pat = r"^\(([^()]+)\)(.+)"
    match = re.match(re_pat, data)
    if match:
        tag = match.group(1)
        name = match.group(2)
    else:
        name = data
    return Unit(tag=tag, name=name)


CustomUnit = Annotated[Unit, BeforeValidator(unit_unserializer)]


def performer_unserializer(data):
    if data:
        return [unit_unserializer(i) for i in data.split(";")]
    else:
        return []


PerformerUnit = Annotated[list[Unit], BeforeValidator(performer_unserializer)]


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
    masterUnit: list[CustomUnit]
    supportUnit: list[CustomUnit]
    otherUnit: list[CustomUnit]
    subUnit: list[CustomUnit]
    showUnit: PerformerUnit


with open("../SearchShowAction.json", encoding="utf-8") as f:
    j = json.loads(f.read())
con = sqlite3.connect("db.sqlite3")
cur = con.cursor()


def query_before_insert(table: str, cols: list[str], values: tuple) -> int:
    cur.execute(f"SELECT * FROM {table} WHERE name=?", (values[0],))
    row = cur.fetchone()
    if row:
        return row[0]
    else:
        ques = ",".join(["?" for i in range(len(cols))])
        cur.execute(f"INSERT INTO {table}({','.join(cols)}) VALUES({ques})", values)

        con.commit()
        return int(cur.lastrowid)


for i in j:
    a = showInfo(**i)
    webNameInd = None
    if a.sourceWebName:
        webNameInd = query_before_insert(
            "Show_sourcewebname", ["name"], (a.sourceWebName,)
        )
    print(a.showUnit)
    cur.execute(
        "INSERT INTO Show_showinfo(show_uid,version,title,category,discount_info,description_filter_html,image_url,web_sales,source_web_promote,comment,edit_modify_date,hit_rate,source_web_name_id) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
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
            webNameInd,
        ),
    )

    for unit in a.supportUnit:
        ind = query_before_insert("Show_unit", ["name"], (unit.name,))
        cur.execute(
            "INSERT INTO Show_supportunit(unit_id,show_uid_id) VALUES(?,?)",
            (ind, a.UID),
        )
    for unit in a.masterUnit:
        ind = query_before_insert("Show_unit", ["name"], (unit.name,))
        cur.execute(
            "INSERT INTO Show_masterunit(unit_id,show_uid_id) VALUES(?,?)", (ind, a.UID)
        )

    for unit in a.subUnit:
        ind = query_before_insert("Show_unit", ["name"], (unit.name,))
        cur.execute(
            "INSERT INTO Show_subunit(unit_id,show_uid_id) VALUES(?,?)", (ind, a.UID)
        )

    for unit in a.otherUnit:
        unit_ind = query_before_insert("Show_unit", ["name"], (unit.name,))
        tag_ind = None
        if unit.tag:
            tag_ind = query_before_insert("Show_tag", ["name"], (unit.tag,))
        cur.execute(
            "INSERT INTO Show_otherunit(unit_id,tag_id,show_uid_id) VALUES(?,?,?)",
            (unit_ind, tag_ind, a.UID),
        )

    for unit in a.showUnit:
        tag_id = None
        if unit.tag:
            tag_id = query_before_insert("Show_country", ["name"], (unit.tag,))

        performer_ind = query_before_insert(
            "Show_performer", ["name", "country_id"], (unit.name, tag_id)
        )
        cur.execute(
            "INSERT INTO Show_showunit(performer_id,show_uid_id) VALUES(?,?)",
            (performer_ind, a.UID),
        )

    for time in a.showInfo:
        cur.execute("SELECT id FROM Show_location WHERE name=?", (time.locationName,))
        row = cur.fetchone()
        if row:
            loaction_ID = row[0]
        else:
            cur.execute(
                """INSERT INTO Show_location
                        (address,name,lat,lng)
                        VALUES (?,?,?,?)""",
                (
                    time.location,
                    time.locationName,
                    float(time.latitude) if time.latitude else None,
                    float(time.longitude) if time.longitude else None,
                ),
            )
            loaction_ID = int(cur.lastrowid)
        cur.execute(
            """INSERT INTO Show_showtime (
            show_uid_id,
            location_id_id,
            time,
            on_sales,
            price,
            end_time)
            VALUES (?,?,?,?,?,?)""",
            (a.UID, loaction_ID, time.time, time.onSales, time.price, time.endTime),
        )
    con.commit()
