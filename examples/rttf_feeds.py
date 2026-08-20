from domaintools import API

api = API(USER_NAME, KEY)

# --- Stream feed (default) ---
# Streams newly observed domains from the last 60 seconds.
results = api.nod(after="-60", top=10)
for line in results.response():
    print(line)

# --- Stream feed with HMAC signing ---
# Uses HMAC-SHA256 instead of the default X-Api-Key header.
# header_authentication is automatically disabled when always_sign_api_key=True.
hmac_api = API(USER_NAME, KEY, always_sign_api_key=True)
results = hmac_api.nod(after="-60", top=10)
for line in results.response():
    print(line)

# --- Stream feed with sessionID ---
# Each subsequent call returns only data since the last request.
results = api.nod(sessionID="my-session", after="-3600", top=10)
for line in results.response():
    print(line)

# --- Download endpoint ---
# Returns a JSON listing of available S3 batch files (not a stream).
result = api.nod(endpoint="download", limit=5)
print(result["download_name"])
for f in result["files"]:
    print(f["name"], f["url"])
