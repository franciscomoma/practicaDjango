import os

import shutil
from PIL import Image
from django.contrib.auth.models import User
from django.test import TestCase
from museum.models import Picture, PictureFile, Size
from django.conf import settings

# Create your tests here.
class TestMuseumBehavior(TestCase):

    def setUp(self):
        settings.UPLOADS_DIR = os.path.join(settings.BASE_DIR, 'test_files')
        os.mkdir(settings.UPLOADS_DIR)

        self.image_5000_x_5000 = Image.new("RGB", (5000, 5000), (255, 0, 0))
        self.image_5000_x_5000.fp = open(os.path.join(settings.UPLOADS_DIR, 'test.jpg'), 'wb')

        self.image_6000_x_6000 = Image.new("RGB", (5000, 5000), (255, 0, 0))
        self.image_6000_x_6000.fp = open(os.path.join(settings.UPLOADS_DIR, 'wow.jpg'), 'wb')

        self.sizes = {
            'big': Size.objects.create(name='big', method=Size.WIDTH, width=3000),
            'small': Size.objects.create(name='small', method=Size.WIDTH, width=1000)
        }
        self.user = User.objects.create(username='red', email='red@pokemon.es', password='charmander')


    def test_create_picture_by_image_creates_a_picture_for_each_size(self):
        picture = Picture.create_picture_by_image(image=self.image_5000_x_5000, user=self.user)

        files = PictureFile.objects.filter(picture=picture)

        self.assertEqual(files.count(), len(self.sizes))

    def test_not_override_image_with_same_filename(self):
        Picture.objects.create(owner=self.user,
                               name='test.jpg',
                               original_file=os.path.join(Picture.get_file_path(), 'test.jpg'))

        picture = Picture.create_picture_by_image(image=self.image_5000_x_5000, user=self.user)

        self.assertEqual(picture.name, 'test_2.jpg')
        self.assertEqual(os.path.basename(picture.original_file.path), 'test_2.jpg')

    def test_delete_all_picture_images_for_a_picture(self):
        picture = Picture.create_picture_by_image(image=self.image_5000_x_5000, user=self.user)

        picture.remove_picture_files()
        files = PictureFile.objects.filter(picture=picture)

        self.assertEqual(files.count(), 0)

    def test_resize_all_picture_files(self):
        picture = Picture.create_picture_by_image(image=self.image_6000_x_6000, user=self.user)

        Size.objects.all().delete()
        Size.objects.create(name='yeah', method=Size.WIDTH, width=200)
        Picture.resize_all_images()
        files = PictureFile.objects.filter(picture=picture)

        self.assertEqual(files.count(), 1)

    def doCleanups(self):
        shutil.rmtree(settings.UPLOADS_DIR)
        super(TestMuseumBehavior, self).doCleanups()
