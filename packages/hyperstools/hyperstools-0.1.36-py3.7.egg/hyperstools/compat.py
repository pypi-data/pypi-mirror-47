# encoding: utf-8

import json
import os

try:
    import django

    isDjango = True
except ImportError:
    isDjango = False

defaultMq = {
    "host": "127.0.0.1",
    "port": "5672",
    "user": "admin",
    "password": "admin",
    "vhost": "/",
    "exchange": "test",
    "queue": "test",
    "routing_key": "test",
}


def close_old_connections():
    pass


if isDjango:
    from django.conf import settings

    try:
        defaultMq = settings.RABBITMQ
        isDjango = True
        django.db.close_old_connections
    except django.core.exceptions.ImproperlyConfigured:
        isDjango = False
if os.environ.get("RABBITMQ"):
    defaultMq = json.loads(os.environ["RABBITMQ"])
