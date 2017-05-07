import os

from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from imageresize.imageexceptions import ImageSizeError
from resizeimage import resizeimage


class Size(models.Model):
    CROP = 'CRP'
    COVER = 'CVR'
    CONTAIN = 'CNT'
    HEIGHT = 'HGT'
    WIDTH = 'WDT'
    THUMBNAIL = 'TMB'

    METHODS = (
        (CROP, _(u'Crop')),
        (COVER, _(u'Cover')),
        (CONTAIN, _('Contain')),
        (HEIGHT, _(u'Height')),
        (WIDTH, _(u'Width')),
        (THUMBNAIL, _(u'Thumbnail')),
    )

    name = models.CharField(max_length=50, primary_key=True)
    method = models.CharField(max_length=3, choices=METHODS, default=WIDTH, verbose_name=_(u'Method'))
    height = models.IntegerField(default=0, verbose_name=_(u'Height'))
    width = models.IntegerField(default=0, verbose_name=_(u'Width'))


class Picture(models.Model):
    created_at = models.DateField(auto_now=True, verbose_name=_(u'Created at'))
    name = models.CharField(max_length=155, verbose_name=_(u'Name'), unique=True)
    owner = models.ForeignKey(User, verbose_name=_(u'Owner'))
    original_file = models.FileField(verbose_name=_(u'File'))

    @staticmethod
    def get_file_path():
        try:
            return settings.UPLOADS_DIR
        except AttributeError as e:
            pass

        try:
            return settings.BASE_DIR
        except AttributeError as e:
            pass

        return ''

    @staticmethod
    def get_file_and_extension(path):
        basename = os.path.basename(path)

        name = os.path.splitext(basename)[0]
        extension = os.path.splitext(basename)[1]

        return {'name': name, 'extension': extension}

    @staticmethod
    def create_picture_by_image(image, user):
        name = os.path.basename(image.fp.name)

        pictures = Picture.objects.filter(name__startswith=os.path.splitext(name)[0])

        if pictures.count() > 0:
            file_attrs = Picture.get_file_and_extension(name)
            name = file_attrs['name'] + '_' + str(pictures.count() + 1) + file_attrs['extension']

        image_path = os.path.join(Picture.get_file_path(), name)
        image.save(image_path)

        picture = Picture.objects.create(name=name,
                                         owner=user,
                                         original_file=image_path)

        picture.resize_image()

        return picture


    def resize_image(self):
        image = Image.open(self.original_file)
        sizes = Size.objects.all()

        for size in sizes:
            try:
                if size.method == Size.WIDTH:
                    resized_image = resizeimage.resize_width(image=image, size=size.width)
                else:
                    continue
            except:
                continue

            name = os.path.basename(self.original_file.path)
            file_attrs = Picture.get_file_and_extension(name)
            resized_path = os.path.join(Picture.get_file_path(), file_attrs['name'] + '_' +
                                        size.name + file_attrs['extension'])
            resized_image.save(resized_path)
            PictureFile.objects.create(picture=self, file=resized_path, size=size)

    @staticmethod
    def resize_all_images():
        for picture in Picture.objects.all():
            picture.remove_picture_files()
            picture.resize_image()

    def remove_picture_files(self):
        for picture in PictureFile.objects.filter(picture=self):
            os.remove(picture.file.path)
            picture.delete()


class PictureFile(models.Model):
    picture = models.ForeignKey(Picture, verbose_name=_(u'Picture'))
    file = models.FileField(verbose_name=_(u'File'))
    size = models.ForeignKey(Size, verbose_name=_(u'Size'))
