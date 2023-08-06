

Url Shortener
=============
[![Build Status](https://travis-ci.org/lil_url.svg?branch=master)](https://travis-ci.org/lil_url)


Current status, version 0.0.1, pre-alpha release
------------------------------------------------

This project is under constant development and maintenance.

Details
-------

Project codebase: <https://github.com/omprakash1989/LilUrl>  

Project Documentation: <http://url_shortner.readthedocs.io/en/latest>  


Features
--------
 - Easy installation
 - No management required for tiny URLs.
 - Easy to use.

Requirements
------------
 - Flask
 - Redis
 - Python (2.7 or above)

Installation
------------
Install lil_url by running: `pip Install Url_shortener`

Contribute
----------

 - Issue Tracker: https://github.com/omprakash1989/LilUrl/issues
 - Source Code: https://github.com/omprakash1989/LilUrl

How to use
==========
- Adding Redis Configuration in settings

```python
REDIS_HOST = '31.236.35.13'
REDIS_PORT = '6379'
BASE_URL = 'https://mybaseurl.com/v1/'

```

- Initialize the app with library.

```python


	from flask import Flask
	from lil_url import init_app

	app = Flask(__name__)
	init_app(app)

```

- Implement the short URL code to the application.

```python


from lil_url import shorten_url
response = shorten_url("https://google.co.in")
if response.get("success"):
	print("Url Slug: {} \n Absolute Url: {}".format(response.get('slug'), response.get('absolute_url')))

```

License
-------
The project is licensed under the MIT License.