from domaintools import API


dt_api = API(USER_NAME, KEY)
query = "SEARCH_HASH"
response = dt_api.iris_investigate(search_hash=query)
results = response['results']
while response['has_more_results']:
    response = dt_api.iris_investigate(search_hash=query, position=response['position'])
    results.extend(response['results'])
print(results)
