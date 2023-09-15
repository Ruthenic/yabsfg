from atproto.firehose import parse_subscribe_repos_message, FirehoseClient
from atproto.firehose.models import MessageFrame
from atproto import CAR, AtUri
from atproto.xrpc_client import models
from atproto.xrpc_client.models import get_or_create, ids, is_record_type
from atproto.xrpc_client.models.utils import get_model_as_dict, get_or_create
from datetime import datetime
from dateutil import parser
import typing, typing as t, sqlite3, config

class FirehoseSubscribeReposClient(FirehoseClient):
    def __init__(self, base_url: t.Optional[str] = None, params: t.Optional[t.Union[dict, 'models.ComAtprotoSyncSubscribeRepos.Params']] = None) -> None:
        params_model = get_or_create(params, models.ComAtprotoSyncSubscribeRepos.Params)

        params_dict = None
        if params_model:
            params_dict = get_model_as_dict(params_model)

        super().__init__(base_url=base_url, method='com.atproto.sync.subscribeRepos', params=params_dict)

client = FirehoseSubscribeReposClient(base_url=config.FIREHOSE_URL)

""" database = {
    "posts": {}
} """
dbconn = sqlite3.connect("feedposts.db")
cur = dbconn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS posts(uri, cid, repo, created_at)")

def on_message_handler(message: MessageFrame) -> None:
    print("recv event")
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
                
                print(record)

                match record.py_type: # type: ignore | GO AWAY
                    case ids.AppBskyFeedPost:
                        record = typing.cast(models.AppBskyFeedPost.Main, record)
                        if config.FILTER(record):
                            cur.execute("INSERT INTO posts VALUES(?, ?, ?, ?)", (str(uri), str(op.cid), commit.repo, parser.parse(record.created_at).timestamp()))
                            print(f"new post just dropped. {record.text} - @{commit.repo} on {record.created_at}")
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