"""Defines all test wide settings and variables"""

import os
import json

from vcr import VCR
from yarl import URL

from domaintools import API, utils


def remove_server(response):
    response.get("headers", {}).pop("server", None)
    response.get("headers", {}).pop("Server", None)
    if "url" in response:
        url = URL(response["url"])
        query = dict(url.query)
        if "api_username" in query:
            query.update(api_username="test")
        if "api_key" in query:
            query.update(api_key="test")
        if "signature" in query:
            query.update(signature="test")
        response["url"] = str(url.with_query(query))
    return response


def filter_patch_parameters(request):
    if request.method == "PATCH" and request.body:
        body = json.loads(request.body)
        body.pop("api_username", None)
        body.pop("api_key", None)
        body.pop("signature", None)
        body.pop("timestamp", None)
        request.body = json.dumps(body).encode("utf-8")
    return request


vcr = VCR(
    before_record_response=remove_server,
    before_record_request=filter_patch_parameters,
    filter_query_parameters=["timestamp", "signature", "api_username", "api_key"],
    filter_post_data_parameters=["timestamp", "signature", "api_username", "api_key"],
    filter_headers=["x-api-key"],
    cassette_library_dir="tests/fixtures/vcr/",
    path_transformer=VCR.ensure_suffix(".yaml"),
    record_mode="new_episodes",
)
with vcr.use_cassette("init_user_account"):
    api = API(
        os.getenv("TEST_USER", "test"),
        os.getenv("TEST_KEY", "test"),
    )

    feeds_api = API(
        os.getenv("TEST_USER", "test"),
        os.getenv("TEST_KEY", "test"),
        rate_limit=False,
    )
