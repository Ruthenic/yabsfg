import config
from datetime import datetime

from atproto import Client, models
from atproto.xrpc_client.models import ids
client = Client()
client.login(config.IDENTIFIER, config.PASSWORD)

response = client.com.atproto.repo.delete_record(models.ComAtprotoRepoDeleteRecord.Data(
    repo=client.me.did, # type: ignore
    collection=ids.AppBskyFeedGenerator,
    rkey=config.ID,
))

print(f"Unpublished feed!")