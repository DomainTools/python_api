from domaintools import API


dt_api = API(USER_NAME, KEY)

# Query a domain
query = "aireamos.org"
response = dt_api.iris_investigate(query)
results = response["results"]
print(results)

# Use the results of that domain to pivot on nameserver host and get all other domains with that nameserver
nameserver_host = results[0]["name_server"][0]["host"]["value"]
response = dt_api.iris_investigate(nameserver_host=nameserver_host)
number_of_domains_with_pivoted_nameserver = response['total_count']
print(number_of_domains_with_pivoted_nameserver)
