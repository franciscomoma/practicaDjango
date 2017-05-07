import datetime

from django.db.models.functions import Lower
from django.http import Http404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import DjangoFilterBackend, OrderingFilter, SearchFilter

from blogs.models import Blog, Post, Category
from blogs.serializers import BlogSerializer, PostSerializer
from blogs.permissions import PostPermissions


class BlogViewSet(ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('owner__username',)
    search_fields = ('posts__title',)
    ordering_fields = ('title', 'posts__title', 'posts__id',)


    def create(self, request, *args, **kwargs):
        blogs = Blog.objects.filter(owner=request.user)

        if blogs.count():
            data = {'error': 'This user owns a blog'}
            return Response(data, status=400)
        else:
            super(BlogViewSet, self).create(request, args, kwargs)

    def perform_create(self, serializer):
        request = self.request
        serializer.save(owner=request.user)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (PostPermissions,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('blog_id',)
    ordering_fields = ('title', 'publish_date')
    search_fields = ('title', 'content')

    def get_queryset(self):
        queryset = super(PostViewSet, self).get_queryset()

        if 'blog_id' in self.kwargs:
            try:
                blog = Blog.objects.get(pk=self.kwargs['blog_id'])
            except:
                raise Http404()

            queryset = queryset.filter(blog=blog)

            if not (blog.owner == self.request.user or self.request.user.is_superuser):
                queryset = queryset.filter(publish_date__lt=datetime.datetime.now())

        queryset.order_by(Lower('publish_date').desc())

        return queryset

    def create(self, request, *args, **kwargs):
        if 'post_id' in kwargs:
            if Post.objects.filter(pk=kwargs['post_id']).exists():
                request.data['related_post'] = int(kwargs['post_id'])

        return super(PostViewSet, self).create(request, args, kwargs)

    def perform_create(self, serializer):
        request = self.request

        try:
            blog = Blog.objects.get(owner=request.user)
        except:
            raise Http404('User must be the owner of a blog')

        try:
            category = Category.objects.get(pk=request.data.get('category'))
        except:
            raise Http404('Category must exists in the platform')

        serializer.save(blog=blog, category=category, publish_date=datetime.datetime.now())

    def perform_update(self, serializer):

        request = self.request

        try:
            category = Category.objects.get(pk=request.data.get('category'))
        except:
            raise Http404('Category must exists in the platform')

        serializer.save(category=category, publish_date=datetime.datetime.now())
