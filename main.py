import config

from atproto import Client, AtUri
xrpc_client = Client()
xrpc_client.login(config.IDENTIFIER, config.PASSWORD)

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
async def get_feed_skeleton(feed: str, limit: int):
    uri = AtUri.from_str(feed)
    if str(uri.hostname) != config.FEED_DID:
        raise HTTPException(status_code=404, detail="fix ur client (requested with incorrect DID)")
    
    if "app.bsky.feed.generator" not in str(uri.pathname):
        raise HTTPException(status_code=404, detail="fix ur client (did not request app.bsky.feed.generator)")
    
    if str(uri.hash) != config.ID:
        raise HTTPException(status_code=404, detail="fix ur client (requested feed does not exist)")

    cur = dbconn.cursor()

    return {
        "feed": config.QUERY(cur, limit)
    }