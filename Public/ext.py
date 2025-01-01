import sqlite3
import os

def init_ext(app):
    pass


def db(sql, params=None):
    conn = sqlite3.connect('Public/sqlite3.db')
    cur = conn.cursor()
    if params:
        cur.execute(sql, params)
    else:
        cur.execute(sql)
    results = cur.fetchall()
    conn.commit()
    conn.close()
    return results



# res = db("SELECT * FROM ali_webhook WHERE timestamp={}".format("1717807966447"))[0]
# print(res)