from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.http import HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect


from blogs.models import Post, Blog
from datetime import datetime
from django.views.generic.edit import CreateView



class PostsListView(ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):
        queryset = super(PostsListView, self).get_queryset()
        queryset = queryset.filter(publish_date__lt=datetime.now())

        if 'username' in self.kwargs:
            try:
                user = User.objects.get(username=self.kwargs.get('username'))
            except User.DoesNotExist:
                return HttpResponseNotFound(render(self.request, '404.html'))

            queryset = queryset.filter(blog__owner=user)

        return queryset.order_by(Lower('publish_date').desc())

    def get_context_data(self, **kwargs):
        context = super(PostsListView, self).get_context_data(**kwargs)

        return context

class PostDetailView(DetailView):
    model = Post

class BlogsListView(ListView):
    model = Blog
    paginate_by = 10

class PostCreation(CreateView):
    model = Post
    fields = ['publish_date', 'title', 'subtitle', 'content', 'summary', 'thumbnail', 'category']

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = request.user

        if user:
            blog = Blog.objects.filter(owner=user)

            if blog.count() != 1:
                pass
        return super(PostCreation, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if not Blog.objects.filter(owner=request.user).exists():
            Blog.objects.create(owner=request.user)

        return super(PostCreation, self).post(request, *args, kwargs)

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        form.instance.blog = Blog.objects.get(owner=self.request.user) # I access with get because I'm sure that it exists thanks to login_required

        response = super(PostCreation, self).form_valid(form)

        return response

