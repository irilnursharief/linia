from config.django.base import *

DEBUG = True
ALLOWED_HOSTS = ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS", default=["127.0.0.1", "localhost", "192.168.100.165"]
)
