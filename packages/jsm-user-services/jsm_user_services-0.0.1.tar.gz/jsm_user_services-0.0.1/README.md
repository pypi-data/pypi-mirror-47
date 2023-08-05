# JSM User JWT Service

Middleware to intercept JWT auth token and more utils functions

## Install

`pip install jsm_user_service`

Add `jsm_user_service` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "jsm_user_services",
    "app_test",
]
```

Add the Middleware:

```python
MIDDLEWARE = [
    ...
    "jsm_user_services.middleware.JsmJwtService",
]
```

## Use

```python
from jsm_user_services.services.user import current_jwt_token
from jsm_user_services.services.user import get_jsm_token
from jsm_user_services.services.user import get_jsm_user_data_from_jwt
from jsm_user_services.services.user import get_ltm_token
from jsm_user_services.services.user import get_ltm_user_data_from_jwt
from jsm_user_services.services.user import get_user_email_from_jwt

current_jwt_token()
get_jsm_token()
get_ltm_token()
get_jsm_user_data_from_jwt()
get_ltm_user_data_from_jwt()
get_user_email_from_jwt()
```
