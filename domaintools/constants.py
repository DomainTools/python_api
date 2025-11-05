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

RTTF_PRODUCTS_LIST = [
    "newly-active-domains-feed-(api)",
    "newly-active-domains-feed-(s3)",
    "newly-observed-domains-feed-(api)",
    "newly-observed-domains-feed-(s3)",
    "newly-observed-hosts-feed-(api)",
    "newly-observed-hosts-feed-(s3)",
    "real-time-domain-hotlist-(api)",
    "real-time-domain-hotlist-(s3)",
    "domain-registration-data-access-protocol-feed-(api)",
    "domain-registration-data-access-protocol-feed-(s3)",
    "real-time-domain-risk-(api)",
    "real-time-domain-risk-(s3)",
    "real-time-domain-discovery-feed-(api)",
    "real-time-domain-discovery-feed-(s3)",
]

RTTF_PRODUCTS_CMD_MAPPING = {
    "newly-active-domains-feed-(api)": "nad",
    "newly-active-domains-feed-(s3)": "nad",
    "newly-observed-domains-feed-(api)": "nod",
    "newly-observed-domains-feed-(s3)": "nod",
    "newly-observed-hosts-feed-(api)": "noh",
    "newly-observed-hosts-feed-(s3)": "noh",
    "real-time-domain-hotlist-(api)": "domainhotlist",
    "real-time-domain-hotlist-(s3)": "domainhotlist",
    "domain-registration-data-access-protocol-feed-(api)": "domainrdap",
    "domain-registration-data-access-protocol-feed-(s3)": "domainrdap",
    "real-time-domain-risk-(api)": "realtime_domain_risk",
    "real-time-domain-risk-(s3)": "realtime_domain_risk",
    "real-time-domain-discovery-feed-(api)": "domaindiscovery",
    "real-time-domain-discovery-feed-(s3)": "domaindiscovery",
}

SPECS_MAPPING = {
    "iris": "domaintools/specs/iris-openapi.yaml",
    # "rttf": "domaintools/specs/feeds-openapi.yaml",
}
