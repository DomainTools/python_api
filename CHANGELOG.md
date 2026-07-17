# Changelog

### 2.9.0
- [NEW] Add support for querying real-time IP feeds (`iphotlist` and `iprisk`).

### 2.8.1
- [FIX] Update python wrapper with a patch that allows the wrapper to proceed with Iris Enrich call even if `account_information` returns a 503 error only (rate limit error).

### 2.8.0
- [NEW] Add IrisQL Support in `iris_investigate` function.
- [NEW] Add `domain_history` command/function in the wrapper.

### 2.7.4
- [FIX] Handle validation error for none value arguments.

### 2.7.3
- [FIX] Issue on missing `risk_score` when passing it on `iris_investigate` function.

### 2.7.2
- [FIX] Issue on importing OpenAPI spec.

### 2.7.0
- [FIX] `iris_investigate` API parity updates (update help documentation)
- [FIX] `iris_investigate` `active` should raise an error as it requires a boolean not a string

### 2.6.0
- [NEW] Implement streaming request for RTTF endpoints to handle the feeds properly and yield the feed line by line and not storing all of it in memory.
- [UPDATE] Test cases.
- [FIX] `available_api_calls` function for RTTF products

### 2.5.3
- [UPDATE] Add IrisQL Support in `iris_investigate` function.
- [UPDATE] Change default Feeds authentication behavior

### 2.5.2
- [FIX] Total count bug for Iris Investigate and Iris Enrich results.

### 2.5.1
- [FIX] Fix for bug found in `realtime_domain_risk` endpoint. Changed product name from `domain-risk-<source>` to `domain-risk-feed-<source>`

### 2.5.0
- [NEW] Add support for Real Time Domain Risk Feed
- [NEW] Add support for Domain Hotlist Feed
- [NEW] Add e2e tests for proxy and ssl
- [UPDATE] Integrate e2e tests in CI pipeline.
- [FIX] Bugs found in `/domainrisk` and `/domainhotlist` endpoints

### 2.4.1
- [UPDATE] Remove support for MD5 based signing.

### 2.4.0
- [NEW] Integrate the NOH Feed to be supportable with the Python Wrapper.
- [NEW] Improve worfklow to automate publishing the package to PyPI.
- [UPDATE] Remove PhishEye.
- [FIX] Improvements on help texts.
- [FIX] Pegged httpxdependency to v.0.28.1 to prevent proxy key error.

### 2.3.0
- [NEW] Integrate the Domain RDAP Feed to be supportable with the Python Wrapper.
- [NEW] Integrate the Domain Discovery Feed to be supportable with the Python Wrapper.
- [UPDATE] Enhancements to RTUF endpoints to support the following: download API, header authentication, csv format.
- [UPDATE] Processing of Iterative Response (HTTP 206) from RTUF endpoints.
- [UPDATE] Help Text and Information Using New Documentation.
- [FIX] Simplification of using the new `proxy` param of httpx.Client. Before we’re using proxy mounts equivalent which we used `proxies` but this was deprecated on httpx v.0.28.x and onward causing errors in the python_wrapper

### 2.0.0
- [NEW] Modernize package - migrate package settings to pyproject.toml
- [NEW] Migrate CLI wrapper to use `typer` library. (CLI comes now with new interface.)
- [NEW] Add support for making `api_url` and `api_port` configurable.
- [NEW] Add `--source-file` or `-s` cli parameter in `iris_investigate` and `iris_enrich` command to support file input instead of long comma-separated domains when typing the domains. Max of **100** domains in a single file.
- [NEW] Add output filtering in `iris_investigate` and `iris_enrich` function in API wrapper (see sample code in `examples/iris_investigate_filter_output.py` folder). Changes includes the ff:
    - Filtering of results "**>=**" to a given `risk_score`.
    - Filtering of results based on `expiration_date` field. (`younger_than_date`, `older_than_date`)
    - Filtering of results based on `updated_after` field.
    - Filtering of results based on a missing field. (include_domains_with_missing_field` or `exclude_domains_with_missing_field`).
- [NEW] Add support on removing/stripping colon in when passing a value in `--ssl_hash` in `iris_investigate` cli command.
- [UPDATE] replace use of upcoming deprecated `datetime.utcnow()` to `timezone.utc`
- [UPDATE] Improve help text in CLI commands.
- [UPDATE] Remove `dateparser` dependency and use native python `datetime` library.
- [FIX] Fix error in `-o` or `--out-file` parameter.

### 1.0.1

- Adds support for the hourly query limit on the Account API endpoint
- Fixes an issue with handling of proxies

### 1.0.0

- Adding support for Iris Detect API endpoints
- Update underlying HTTP client
- Addition of helper functions for common tasks
- Documentation and example code updates

### 0.6.2

- Update README with Iris trademarks

### 0.6.1

- Fix an invalid response type error for available_api_calls on CLI
- Add better error messaging for users when proxy info is not set correctly
- Fix typo on limit_exceeded when outputting formats other than JSON when using non-async results

### 0.6.0

### 0.3.3

- Python 3.5.2 installation fix

### 0.3.1

- Python 3.7.0 Python version check for async fixed

### 0.3.0

- Python 3.7 support as well as general Async fixes and improvements (Thanks @jnwatson)

### 0.2.4

- Enabled rate-limiting support for Iris API endpoints

### 0.2.3

- Added support for Iris Investigate and Enrich

### 0.2.2

- HTTP Authentication fixes
- Initial proxy support

### 0.2.1

- Separated out IncompleteResponseException; enabling partial results to still be read
- Fixed unknown exception handling

### 0.2.0

- Ensure connections are cleaned up

### 0.1.9

- Added support for `risk` and `risk_evidence` API calls

### 0.1.8

- Updated defaults for domain_search call

### 0.1.7

- Fixed typo in registrar information assignment

### 0.1.6

- Added support for Iris endpoint

### 0.1.5

- Made Results a subclass of both MutableMapping and MutableSequence for more natural interaction

### 0.1.4

- Wait to make account information call for rate limiting till a call is made against another API endpoint

### 0.0.1

- Initial Release
