from atproto.firehose import FirehoseSubscribeReposClient, parse_subscribe_repos_message
from atproto.firehose.models import MessageFrame
from atproto import CAR, AtUri
from atproto.xrpc_client import models
from atproto.xrpc_client.models import get_or_create, ids, is_record_type
from datetime import datetime
from dateutil import parser
import typing, sqlite3, config

client = FirehoseSubscribeReposClient()

""" database = {
    "posts": {}
} """
dbconn = sqlite3.connect("feedposts.db")
cur = dbconn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS posts(uri, cid, repo, created_at)")

def on_message_handler(message: MessageFrame) -> None:
    commit = parse_subscribe_repos_message(message)
    if not isinstance(commit, models.ComAtprotoSyncSubscribeRepos.Commit):
        # is it possible to *not* have one of these? god knows, but the example does it so we do too
        return
    car = CAR.from_bytes(commit.blocks) # type: ignore | cry
    cur = dbconn.cursor()
    for op in commit.ops:
        uri = AtUri.from_str(f'at://{commit.repo}/{op.path}')

        match op.action:
            case "create":
                if not op.cid or not car.blocks.get(op.cid):
                    continue

                
                record = get_or_create(car.blocks.get(op.cid), strict=False)
                
                match record._type: # type: ignore | GO AWAY
                    case ids.AppBskyFeedPost:
                        record = typing.cast(models.AppBskyFeedPost.Main, record)
                        if config.FILTER(record):
                            cur.execute("INSERT INTO posts VALUES(?, ?, ?, ?)", (str(uri), str(op.cid), commit.repo, parser.parse(record.createdAt).timestamp()))
                            print(f"new post just dropped. {record.text} - @{commit.repo} on {record.createdAt}")
                        continue
                    case _:
                        continue
            
            case "delete":
                match uri.collection:
                    case ids.AppBskyFeedPost:
                        cur.execute("DELETE FROM posts WHERE uri = ?", (str(uri),))
                        continue
                    case _:
                        continue
            
            case _:
                continue
    dbconn.commit()

async def main():
    client.start(on_message_handler)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())