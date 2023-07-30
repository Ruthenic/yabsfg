import sqlite3
from typing import List

def fandom(cur: sqlite3.Cursor, limit: int) -> List[str]:
    posts = cur.execute("SELECT uri FROM posts ORDER BY created_at DESC").fetchmany(size=limit)
    res = []
    for post in posts:
        res.append({
            "post": post[0]
        })
    return res