import datetime

from django.db.models.functions import Lower
from rest_framework import serializers
from blogs.models import Blog, Post
from utils.serializers import FilteredReverseRelationSerializer


class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='post-detail')

    class Meta:
        model = Post
        fields = ('url', 'title', 'publish_date', 'summary', 'thumbnail', 'content', 'related_post')

    def get_fields(self):
        fields = super(PostSerializer, self).get_fields()

        if 'view' in self.context:
            if self.context['view'].action in ('create', 'update'):
                fields.pop('publish_date')
                fields.pop('thumbnail')
            if self.context['view'].action in ('list'):
                fields.pop('content')

        return fields


class BlogSerializer(FilteredReverseRelationSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='blog-detail')
    posts = PostSerializer(many=True)

    class Meta:
        model = Blog
        fields = '__all__'

    def apply_user_reverse_relation_filters(self, queryset, request, parent):
        if request:
            user = request.user

            if not (parent.owner == user or (user.is_authenticated() and user.is_superuser)):
                queryset = queryset.filter(publish_date__lt=datetime.datetime.now())

            queryset.order_by(Lower('publish_date').desc())

        return queryset

    def get_fields(self):
        fields = super(BlogSerializer, self).get_fields()

        if 'view' in self.context:
            if self.context['view'].action in ('list'):
                fields.pop('posts')
            if self.context['view'].action in ('create', 'update'):
                fields.pop('posts')
                fields.pop('owner')

        return fields
