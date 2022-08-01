# Changelog

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
