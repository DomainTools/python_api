Changelog
=========
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
