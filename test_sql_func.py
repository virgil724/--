import sqlite3

con = sqlite3.connect("test.db")
cur = con.cursor()


def query_before_insert(table: str, cols: list[str], values: tuple) -> int:
    cur.execute(f"SELECT * FROM {table} WHERE name=?", (values[0],))
    row = cur.fetchone()
    if row:
        return row[0]
    else:
        ques = ",".join(["?" for i in range(len(cols))])
        print(values)
        cur.execute(f"INSERT INTO {table}({','.join(cols)}) VALUES({ques})", values)

        con.commit()
        return int(cur.lastrowid)


a=query_before_insert("MASTER_UNIT", ["name", "show_uid"], ("環球音樂132","1234"))

print(a)