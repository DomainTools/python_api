from domaintools import API


dt_api = API('wagena-api-test-user', 'eee30-51701-98ecb-89002-69d16')
result = dt_api.iris_investigate(domains='int-chase.com').data()
print(result)
