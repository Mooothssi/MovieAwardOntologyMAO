import os

from django.apps import apps
from django.conf import settings


def start_django_lite():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mao_dj.mysite.settings")
    if not apps.loading:
        apps.populate(settings.INSTALLED_APPS)


if __name__ == '__main__':
    start_django_lite()
