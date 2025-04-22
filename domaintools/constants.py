from enum import Enum


class Endpoint(Enum):
    FEED = "feed"
    DOWNLOAD = "download"


class Source(Enum):
    API = "api"
    S3 = "s3"


class OutputFormat(Enum):
    JSONL = "jsonl"
    CSV = "csv"


HEADER_ACCEPT_KEY_CSV_FORMAT = "text/csv"

ENDPOINT_TO_SOURCE_MAP = {
    Endpoint.FEED.value: Source.API,
    Endpoint.DOWNLOAD.value: Source.S3,
}

FEEDS_PRODUCTS_LIST = [
    "newly-active-domains-feed-(api)",
    "newly-active-domains-feed-(s3)",
    "newly-observed-domains-feed-(api)",
    "newly-observed-domains-feed-(s3)",
    "newly-observed-hosts-feed-(api)",
    "newly-observed-hosts-feed-(s3)",
    "domain-hotlist-feed-(api)",
    "domain-hotlist-feed-(s3)",
    "domain-registration-data-access-protocol-feed-(api)",
    "domain-registration-data-access-protocol-feed-(s3)",
    "domain-risk-feed-(api)",
    "domain-risk-feed-(s3)",
    "real-time-domain-discovery-feed-(api)",
    "real-time-domain-discovery-feed-(s3)",
]
