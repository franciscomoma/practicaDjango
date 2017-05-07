import os
import re

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from notify.notify import send_email


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
    related_post = models.ForeignKey('self', null=True, blank=True)

    mention_email_body = _("Hello {0}. Someone mention you on post {1}.")
    mention_email_subject = _("Someone mention you")
    answer_email_body = _("Hello {0}. Someone answer you on post {1}.")
    answer_email_subject = _("Someone answer you")

    mention_regex = re.compile('(@[a-zA-ZñÑ0-9]+)')

    def get_users_mentioned_on_post(self):
        mentions = self.mention_regex.findall(self.content)

        users = []
        for mention in mentions:
            mention = mention.replace('@', '')

            users_found = User.objects.filter(username=mention)

            if len(users_found) >= 1:
                if len(users_found) > 1:
                    print("We found more than one users with the same username. Only notify the first.")

                users.append(users_found[0])

        return users

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        send_notifications = False
        if not self.pk:
            send_notifications = True

        super(Post, self).save(force_insert=force_insert, force_update=force_update,
                               using=using, update_fields=update_fields)

        if send_notifications:
            if self.related_post and self.blog.owner != self.related_post.blog.owner:
                answered_user = self.related_post.blog.owner
                if answered_user.email:
                    send_email(answered_user.email,
                               self.answer_email_subject,
                               self.answer_email_body.format(answered_user.username,
                                                             self.pk))

            for mentioned_user in self.get_users_mentioned_on_post():
                if mentioned_user.email:
                    send_email(mentioned_user.email,
                               self.mention_email_subject,
                               self.mention_email_body.format(mentioned_user.username,
                                                              self.pk))
