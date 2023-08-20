from typing import Optional
import typing
import config
from atproto import Client, AtUri

client = Client()
client.login(config.IDENTIFIER, config.PASSWORD)

from fastapi import FastAPI, HTTPException
import sqlite3

dbconn = sqlite3.connect("feedposts.db")
cur = dbconn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS posts(uri, cid, repo, created_at)")

app = FastAPI()

@app.get("/.well-known/did.json")
async def get_did_doc():
    return {
        "@context": ["https://www.w3.org/ns/did/v1"],
        "id": config.FEED_DID,
        "service": [{
            "id": "#bsky_fg",
            "type": "BskyFeedGenerator",
            "serviceEndpoint": config.PUBLIC_LOCATION
        }]
    }

@app.get("/xrpc/app.bsky.feed.getFeedSkeleton")
async def get_feed_skeleton(feed: str, limit: int, cursor: Optional[str] = None):
    uri = AtUri.from_str(feed)
    print (uri.pathname)
    if str(uri.hostname) != config.FEED_DID and str(uri.hostname) != client.me.did: # type: ignore
        raise HTTPException(status_code=404, detail="fix ur client (requested with incorrect DID)")
    
    if "app.bsky.feed.generator" not in str(uri.pathname).split("/")[1]:
        raise HTTPException(status_code=404, detail="fix ur client (did not request app.bsky.feed.generator)")
    
    if str(uri.pathname).split("/")[2] != config.ID:
        raise HTTPException(status_code=404, detail="fix ur client (requested feed does not exist)")

    cur = dbconn.cursor()

    newcursor = 0

    if cursor:
        newcursor = int(cursor)

    res = config.QUERY(cur, limit, newcursor)

    return {
        "feed": res[0],
        "cursor": str(res[1])
    }