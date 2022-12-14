![pytest](https://github.com/preritdas/personal-api/actions/workflows/pytest.yml/badge.svg)
![coverage](tests/badge.svg)
![docs](https://github.com/preritdas/personal-api/actions/workflows/docs.yml/badge.svg)
![gcp](https://github.com/preritdas/personal-api/actions/workflows/google-cloud.yml/badge.svg)


# Personal API

Documentation: [api.preritdas.com](https://api.preritdas.com). 


## Notes

(This is for personal reference.)

### To do

[ ] Docs for `billsplit` app.


### Versions

[ ] Translation is currently disabled because when installing the `translators` library in Python 3.11, building `lxml` fails. There is no active change to production behavior for now because translation is disabled in [config](config.py).

### CI/CD

[ ] Tests are passing on Python 3.11. CI tests are held at Python 3.10 as that's the latest runtime currently supported on App Engine. Once App Engine supports the Python 3.11 runtime, both the runtimes on App Engine and CI here will be bumped.

### Tests

Tests can be run out of the box (with all the [requirements](tests/requirements.txt)) with the `pytest` command (or `python -m pytest`). For coverage, use `pytest --cov`, and for an html coverage report, use `pytest --cov --covreport html`. 

For VS Code testing integration, include these lines in `.vscode/setings.json`.

```json
{
    "python.testing.pytestArgs": [
        "--cov",
        "--cov-report=html"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "python.testing.pytestEnabled": true,
}
```

This will automatically generate an html coverage report whenever tests are run.

Also, the following script can be used to check if production databases were modified because of a test. (Make sure the API is down before trusting the results.)

```python
import pytest

from permissions import permissions_db
from usage import usage_db
from apps.groceries import grocery_db
from apps.billsplit.billsplit_db import db as billsplit_db


# Store original content and states
databases = [permissions_db, usage_db, grocery_db, billsplit_db]
pre_content = [db.fetch() for db in databases]

# Run tests
pytest.main()

# Compare
assert all([db.fetch() == pre for db, pre in zip(databases, pre_content)])
```

### Notes

- Try not to run tests concurrently as objects are created in the production database and tested against. For example, if two tests are run at the same time, and both tests create a temporary user in the permissions database, one or both of the tests should fail as a `QueryError` would be raised on discovering duplicate users (when not expected).

## Style Guide

(This is for personal reference.)

Each app needs a `handler` function callable under the app level, ex. in an app module's `__init__.py`. The handler *must* take exactly two arguments, `content: str` and `options: dict`. Content is the inbound message's raw content. The handler must return string content to be texted back to the user. The main handler always passes an `inbound_phone` key in the `options` dictionary to each app.

```python
# Default options payload
options: dict[str, str] = {
    "inbound_phone": "12223334455"
}
```

This same structure is used in tests. The below is a series of inter-dependent fixtures with the same `default_options` format, using a randomly generated phone number that lasts for the duration of the tests (in the permissions database as well).

https://github.com/preritdas/personal-api/blob/9c60f54b6db8c4aa7c80ecd05e328fe5b868b946/tests/conftest.py#L12-L26

Read options with `dict.get` supplying a default option value if the option isn't provided. For example, WordHunt options in the handler...

https://github.com/preritdas/personal-api/blob/a5ff2d2af5b567d0a2dac8b20cddce4a12064f3a/wordhunt/__init__.py#L4-L10

A handler's function signature should be as follows.

```python
def handler(content: str, options: dict[str, str]) -> str
```
