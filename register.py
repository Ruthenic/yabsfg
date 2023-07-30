import config
from datetime import datetime

from atproto import Client, models
from atproto.xrpc_client.models import ids
client = Client()
client.login(config.IDENTIFIER, config.PASSWORD)

response = client.com.atproto.repo.put_record(models.ComAtprotoRepoPutRecord.Data(
    repo=client.me.did, # type: ignore
    collection=ids.AppBskyFeedGenerator,
    rkey=config.ID,
    record=models.AppBskyFeedGenerator.Main(
        did=config.FEED_DID,
        displayName=config.NAME,
        description=config.DESCRIPTION,
        createdAt=datetime.now().isoformat(),
    )
))

print(f"Published at {response.uri}!")