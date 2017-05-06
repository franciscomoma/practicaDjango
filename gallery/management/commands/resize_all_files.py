# -*- coding: utf-8 -*-
from gallery.tasks import museum_resize_all_images
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        museum_resize_all_images.delay()


