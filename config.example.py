from modules import filter_func, query

# bsky info
BASE_URL = None # manually set pds url, otherwise bsky.social
FIREHOSE_URL = None # manually set pds/bgs url for firehose, otherwise bsky.social
IDENTIFIER = "YOUR_USERNAME.bsky.social"
PASSWORD = "YOUR_PASSWORD" # please use an app password and not your real one

# feed metadata
ID = "FEED_ID"
NAME = "Example Feed Here"
DESCRIPTION = "Example feed made with YABSFG"

# feed non-meta data
PUBLIC_LOCATION = "URL_GOES_HERE" # url where the feed can be publicly accessed (probably needs to be https)

# custom db insertion filter/feed request query hooks
# please replace with custom functions if you don't want to make another fandom list!
FILTER = filter_func.fandom
QUERY = query.fandom

# no touchy
FEED_DID = f"did:web:{PUBLIC_LOCATION.lstrip('https://')}"
