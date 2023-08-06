import os

BOT_CONFIG = {
    "REDIS": {
        "HOST": 'localhost',
        "PORT": 6379,
        "PASSWORD": None,
    },
    "INTERFACES": [
        "botshot.tests.test_chat_manager._TestInterface",
    ],
    "GREETING_INTENT": "default",
    "TELEGRAM_TOKEN": "foo"
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

SECRET_KEY = "foo"

INSTALLED_APPS = (
    'botshot',
)

USE_TZ = True
