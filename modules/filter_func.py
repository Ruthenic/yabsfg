from atproto.xrpc_client import models
import re

def fandom(record: models.AppBskyFeedPost.Main) -> bool:
    return bool(re.match(r'(helluva\s*boss)|(hazbin\s*hotel)|(murder\s*drones)|(serial\s*designation)|(bendy and the ink\s*machine)|(\s+batim)|(#batim)|(batdr)|(ink\s*demon)|(ultrakill)', record.text, flags=re.IGNORECASE))