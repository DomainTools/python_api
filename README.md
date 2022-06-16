![domaintools](https://github.com/DomainTools/python_api/raw/main/artwork/logo.png)
===================

[![PyPI version](https://badge.fury.io/py/domaintools_api.svg)](http://badge.fury.io/py/domaintools_api)
[![CI Status](https://github.com/domaintools/python_api/workflows/Tests/badge.svg)](https://github.com/domaintools/python_api/actions)
[![Coverage Status](https://coveralls.io/repos/github/DomainTools/python_api/badge.svg?branch=main)](https://coveralls.io/github/DomainTools/python_api?branch=main)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/domaintools_api/)

DomainTools Official Python API

![domaintools Example](https://github.com/DomainTools/python_api/raw/main/artwork/example.gif)

The DomainTools Python API Wrapper provides an interface to work with our cybersecurity and related data tools provided by our Iris Investigate™, Iris Enrich™, and Iris Detect™ products. It is actively maintained and may be downloaded via <a href="https://github.com/DomainTools/python_api">GitHub</a> or <a href="https://pypi.org/project/domaintools-api/">PyPI</a>. See the included README file, the examples folder, and API documentation (https://app.swaggerhub.com/apis-docs/DomainToolsLLC/DomainTools_APIs/1.0#) for more info.

Installing the DomainTools API
===================

To install the API run

```bash
pip install domaintools_api --upgrade
```

Ideally, within a virtual environment.


Using the API
===================

To start out create an instance of the API - passing in your credentials

```python

from domaintools import API


api = API(USER_NAME, KEY)
```

Every API endpoint is then exposed as a method on the API object, with any parameters that should be passed into that endpoint
being passed in as method arguments:

```python
api.iris_enrich('domaintools.com')
```

You can get an overview of every endpoint that you can interact with using the builtin help function:

```python
help(api)
```

Or if you know the endpoint you want to use, you can get more information about it:

```python
help(api.iris_investigate)
```

If applicable, native Python looping can be used directly to loop through any results:

```python
for result in api.iris_enrich('domaintools.com').response().get('results', {}):
    print(result['domain'])
```

You can also use a context manager to ensure processing on the results only occurs if the request is successfully made:

```python
with api.iris_enrich('domaintools.com').response().get('results', {}) as results:
    print(results)
```

For API calls where a single item is expected to be returned, you can directly interact with the result:

```python
profile = api.domain_profile('google.com')
title = profile['website_data']['title']
```

For any API call where a single type of data is expected you can directly cast to the desired type:

```python
float(api.reputation('google.com')) == 0.0
int(api.reputation('google.com')) == 0
```

The entire structure returned from DomainTools can be retrieved by doing `.data()` while just the actionable response information
can be retrieved by doing `.response()`:

```python
api.iris_enrich('domaintools.com').data() == {'response': { ... }}
api.iris_enrich('domaintools.com').response() == { ... }
```

You can directly get the html, xml, or json version of the response by calling `.(html|xml|json)()` These only work with non AsyncResults:
```python
json = str(api.domain_search('google').json())
xml = str(api.domain_search('google').xml())
html = str(api.domain_search('google').html())
```

If any API call is unsuccesfull, one of the exceptions defined in `domaintools.exceptions` will be raised:

```python-traceback
api.domain_profile('notvalid').data()


---------------------------------------------------------------------------
BadRequestException                       Traceback (most recent call last)
<ipython-input-3-f9e22e2cf09d> in <module>()
----> 1 api.domain_profile('google').data()

/home/tcrosley/projects/external/python_api/venv/lib/python3.5/site-packages/domaintools-0.0.1-py3.5.egg/domaintools/base_results.py in data(self)
     25                 self.api._request_session = Session()
     26             results = self.api._request_session.get(self.url, params=self.kwargs)
---> 27             self.status = results.status_code
     28             if self.kwargs.get('format', 'json') == 'json':
     29                 self._data = results.json()

/home/tcrosley/projects/external/python_api/venv/lib/python3.5/site-packages/domaintools-0.0.1-py3.5.egg/domaintools/base_results.py in status(self, code)
     44
     45         elif code == 400:
---> 46             raise BadRequestException()
     47         elif code == 403:
     48             raise NotAuthorizedException()

BadRequestException:

```

the exception will contain the status code and the reason for the exception:

```python
try:
    api.domain_profile('notvalid').data()
except Exception as e:
    assert e.code == 400
    assert 'We could not understand your request' in e.reason['error']['message']
```

You can get the status code of a response outside of exception handling by doing `.status`:

```python

api.domain_profile('google.com').status == 200
```

Using the API Asynchronously
===================

![domaintools Async Example](https://github.com/DomainTools/python_api/raw/main/artwork/example_async.gif)

The DomainTools API automatically supports async usage:

```python

search_results = await api.iris_enrich('domaintools.com').response().get('results', {})
```

There is built-in support for async context managers:

```python
async with api.iris_enrich('domaintools.com').response().get('results', {}) as search_results:
    # do things
```

And direct async for loops:

```python
async for result in api.iris_enrich('domaintools.com').response().get('results', {}):
    print(result)
```

All async operations can safely be intermixed with non async ones - with optimal performance achieved if the async call is done first:
```python
profile = api.domain_profile('google.com')
await profile
title = profile['website_data']['title']
```

Interacting with the API via the command line client
===================

![domaintools CLI Example](https://github.com/DomainTools/python_api/raw/main/artwork/example_cli.gif)

Immediately after installing `domaintools_api` with pip, a `domaintools` command line client will become available to you:

```bash
domaintools --help
```

To use - simply pass in the api_call you would like to make along with the parameters that it takes and your credentials:

```bash
domaintools iris_investigate --domains domaintools.com -u $TEST_USER -k $TEST_KEY
```

Optionally, you can specify the desired format (html, xml, json, or list) of the results:

```bash
domaintools domain_search google --max_length 10 -u $TEST_USER -k $TEST_KEY -f html
```

To avoid having to type in your API key repeatedly, you can specify them in `~/.dtapi` separated by a new line:

```bash
API_USER
API_KEY
```

Python Version Support Policy
===================

Please see the [supported versions](https://github.com/DomainTools/python_api/raw/main/PYTHON_SUPPORT.md) document 
for the DomainTools Python support policy.
