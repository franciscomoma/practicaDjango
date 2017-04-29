from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


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
    name = models.CharField(max_length=155, verbose_name=_(u'Name'))
    owner = models.OneToOneField(User, verbose_name=_(u'Owner'))


class PictureFile(models.Model):
    picture = models.ForeignKey(Picture, verbose_name=_(u'Picture'))
    file = models.FileField(verbose_name=_(u'File'))
    size = models.ForeignKey(Size, verbose_name=_(u'Size'))
