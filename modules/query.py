import sqlite3
from typing import List, Tuple, Optional

def fandom(cur: sqlite3.Cursor, limit: int, index: int) -> Tuple[List[str], Optional[int]]:
    posts = cur.execute(f"SELECT uri FROM posts ORDER BY created_at DESC LIMIT {limit} OFFSET {index}").fetchmany(size=limit)
    res = []
    for post in posts:
        res.append({
            "post": post[0]
        })

    if len(res) < limit:
        return (res, None)
    else:
        return (res, index+limit)