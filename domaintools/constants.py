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
