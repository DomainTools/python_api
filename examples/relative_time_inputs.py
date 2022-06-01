from domaintools import API
from dateparser import parse


dt_api = API(USER_NAME, KEY)
# Using dateparser to parse a relative time input.
# See: https://dateparser.readthedocs.io/en/latest/introduction.html#relative-dates
now = parse("now")
print(now)
last_week = parse("1 week ago")
print(last_week)
# You can then use the parsed date as a parameter for the API.
result = dt_api.iris_detect_new_domains(discovered_since=last_week, preview=True, sort=["discovered_date"], order="asc").data()
print(result)

# Should work with any place a datetime can be passed in.
result = dt_api.iris_investigate(domains="0-6.xyz", data_updated_after=last_week).data()
print(result)
