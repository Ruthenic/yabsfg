from atproto.xrpc_client import models
import re

def search_with_flags(regex: str, content: str) -> bool:
    return bool(re.search(regex, content, flags=re.IGNORECASE))

def anything(_: models.AppBskyFeedPost.Main) -> bool:
    return True

def fandom(record: models.AppBskyFeedPost.Main) -> bool:
    # basic hellaverse matching
    if search_with_flags(r'(helluva\s*boss)|(hazbin\s*hotel)|(hellaverse)', record.text):
        return True
    
    # hellaverse specific character matching
    if search_with_flags(r'(stolas)|(blitz(o|ø))|(fizzarolli)|(cash\s*buckzo)', record.text):
        return True
    
    # murder drones
    if search_with_flags(r'(murder\s*drones)|(serial\s*designation)', record.text):
        return True
    
    # batim
    if search_with_flags(r'(bendy\s*and\s*the\s*ink\s*machine)|(\s+batim\s+)|(#batim)|(batdr)|(ink\s*demon)', record.text):
        return True
    
    # ultrakill
    if search_with_flags(r'(ultrakill)|(minos\s*prime)|(sisyphus\s*prime)', record.text):
        return True
        
    return False