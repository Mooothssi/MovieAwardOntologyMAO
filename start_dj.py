import os

from django.apps import apps
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mao_dj.mysite.settings")
if not apps.loading:
    apps.populate(settings.INSTALLED_APPS)
