from domaintools import API


dt_api = API(USER_NAME, KEY)
result = dt_api.iris_enrich('google.com').data()
print(result)
