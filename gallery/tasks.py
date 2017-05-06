import base64
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from celery import Celery

# set the default Django settings module for the 'celery' program.

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fblog.settings")

app = Celery('fblog', broker='amqp://localhost')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

import django
django.setup()

from PIL import Image
from museum.models import Picture
from django.contrib.auth.models import User


@app.task
def museum_create_picture_by_image(image, user):
    Picture.create_picture_by_image(Image.open(image), User.objects.get(pk=user))
    os.remove(image)
    print('BACKGROUND TASK FINISHED!')


@app.task
def museum_resize_all_images():
    Picture.resize_all_images()
    print('BACKGROUND TASK FINISHED!')
