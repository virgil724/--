import sqlite3

con = sqlite3.connect("test.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE SHOW_INFO(show_uid,version,title,category,discount_info,description_filter_html,image_url,web_sales,source_web_promote,comment,edit_modify_date,hit_rate,UNIQUE(show_uid))"
)
#!　#################
cur.execute("""
CREATE TABLE MASTER_UNIT(
            name,
            show_uid ,
            FOREIGN KEY(show_uid) REFERENCES SHOW_INFO(show_uid)
)
""")
cur.execute("""
CREATE TABLE SUPPORT_UNIT(
            name,
            show_uid ,
            FOREIGN KEY(show_uid) REFERENCES SHOW_INFO(show_uid)
)
""")
cur.execute("""
CREATE TABLE SUB_UNIT(
            name,
            show_uid ,
            FOREIGN KEY(show_uid) REFERENCES SHOW_INFO(show_uid)
)
""")
cur.execute("""
CREATE TABLE OTHER_UNIT(
            name,
            show_uid ,
            FOREIGN KEY(show_uid) REFERENCES SHOW_INFO(show_uid)
)
""")

cur.execute("""
CREATE TABLE SHOW_UNIT(
            name,
            show_uid ,
            FOREIGN KEY(show_uid) REFERENCES SHOW_INFO(show_uid)
)
""")

cur.execute("""
CREATE TABLE SOURCE_WEB_NAME(
            name,
            show_uid ,
            FOREIGN KEY(show_uid) REFERENCES SHOW_INFO(show_uid)
)
""")
#! ########################


cur.execute("""
CREATE TABLE LOCATION(
            location_id INTEGER PRIMARY KEY AUTOINCREMENT,
            address,
            name,
            lat,
            lng
)
""")


cur.execute("""
CREATE TABLE SHOW_TIME(
            time_id,
            show_uid,
            location_id,
            time,
            on_sales,
            price,
            end_time,
            FOREIGN KEY(show_uid) REFERENCES SHOW_INFO(show_uid),
            FOREIGN KEY(location_id) REFERENCES LOCATION(location_id)
)
""")
