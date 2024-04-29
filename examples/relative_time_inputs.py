from domaintools import API
from datetime import datetime, timedelta


dt_api = API(USER_NAME, KEY)
# Suggestion: you can try to use dateparser to parse a relative time input.
# See: https://dateparser.readthedocs.io/en/latest/introduction.html#relative-dates
now = datetime.now()
print(now)
last_week = datetime.now() - timedelta(days=7)
print(last_week)
# You can then use the parsed date as a parameter for the API.
result = dt_api.iris_detect_new_domains(
    discovered_since=last_week, preview=True, sort=["discovered_date"], order="asc"
).data()
print(result)

# Should work with any place a datetime can be passed in.
result = dt_api.iris_investigate(domains="0-6.xyz", data_updated_after=last_week).data()
print(result)
