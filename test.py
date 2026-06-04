import os

from domaintools import API

user = os.getenv("MY_API_USER", "jbabac")
key = os.getenv("MY_API_KEY")

dt_api = API(
    username=user,
    key=key,
    app_name="jd-test-python-wrapper",
)

result = dt_api.iris_investigate("espn.com").data()
print(result)

# help(dt_api.iris_investigate)
