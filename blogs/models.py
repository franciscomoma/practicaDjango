import os

from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=15, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Blog(models.Model):
    created_at = models.DateField(auto_now=True)
    title = models.CharField(max_length=155)
    owner = models.OneToOneField(User)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return u'Blog of ' + self.owner.username

    def __str__(self):
        return 'Blog of ' + self.owner.username

class Post(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField()
    blog = models.ForeignKey(Blog, related_name='posts', related_query_name='posts')
    title = models.CharField(max_length=155)
    subtitle = models.CharField(max_length=155)
    content = models.TextField()
    summary = models.CharField(max_length=155)
    thumbnail = models.FilePathField(path=os.path.join('static', 'uploads'), allow_folders=False, match='.+(.png|.jpg)$', null=True, blank=True, default=None)
    category = models.ForeignKey(Category)
