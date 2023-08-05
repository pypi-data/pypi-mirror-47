# Class for autotests flask python apps

[![Python 2.7.14 3.6.3 3.7](https://img.shields.io/travis/vb64/test.helper.flask.svg?label=Python%202.7%203.6%203.7&style=plastic)](https://travis-ci.org/vb64/test.helper.flask)
[![Code Climate](https://img.shields.io/codeclimate/maintainability-percentage/vb64/test.helper.flask.svg?label=Code%20Climate&style=plastic)](https://codeclimate.com/github/vb64/test.helper.flask)
[![Coverage Status](https://coveralls.io/repos/github/vb64/test.helper.flask/badge.svg?branch=master)](https://coveralls.io/github/vb64/test.helper.flask?branch=master)

## Install
```
$ pip install tester_flask
```

## Usage in tests

```python
from flask import Flask
from tester_flask import TestFlask

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return "Flask OK"


@app.route('/redirect', methods=['POST'])
def redirect_page():
    return redirect(url_for('main_page'))


class TestFlaskApp(TestFlask):
    """
    test flask app
    """
    def setUp(self):
        TestFlask.setUp(self, app)

    def test_app(self):
        self.assertEqual(self.simple_view('main_page').status_code, 200)
        self.assertEqual(self.param_post('main_page', {'hello': 1}, {'one': 1}).status_code, 200)

        response = self.simple_post('redirect_page', {'one': 1}, follow=False)
        self.assertEqual(self.final_url(response), self.get_url('main_page'))

```

## Development
```
$ git clone git@github.com:vb64/test.helper.flask.git
$ cd test.helper.flask
```

With Python 2.7
```
$ make setup PYTHON_BIN="/path/to/python2.7 -m virtualenv"
```

With Python 3
```
$ make setup PYTHON_BIN="/path/to/python3.7 -m venv"
```

Then
```
$ make tests
```
