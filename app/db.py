import json
import sqlite3
import time
from contextlib import closing
from pathlib import Path

from .config import DB_PATH


def _conn():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init():
    with closing(_conn()) as c, c:
        c.execute("create table if not exists cache(key text primary key, value text, ts real)")
        c.execute("create table if not exists analyses(id text primary key, data text, ts real)")


def cache_get(key, ttl_hours):
    with closing(_conn()) as c:
        row = c.execute("select value, ts from cache where key=?", (key,)).fetchone()
    if row and time.time() - row[1] < ttl_hours * 3600:
        return json.loads(row[0])
    return None


def cache_set(key, value):
    with closing(_conn()) as c, c:
        c.execute("insert or replace into cache values(?,?,?)", (key, json.dumps(value), time.time()))


def save_analysis(aid, data):
    with closing(_conn()) as c, c:
        c.execute("insert or replace into analyses values(?,?,?)", (aid, json.dumps(data), time.time()))


def get_analysis(aid):
    with closing(_conn()) as c:
        row = c.execute("select data from analyses where id=?", (aid,)).fetchone()
    return json.loads(row[0]) if row else None
