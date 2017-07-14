from rest_framework import routers

"""fblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from blogs.views import PostsListView, PostDetailView, BlogsListView, PostCreation
from blogs.api import BlogViewSet, PostViewSet
from users.views import do_login, do_logout, RegisterView
from users.api import UserViewSet
from gallery.api import ImageUploadView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'blogs', BlogViewSet)
router.register(r'posts', PostViewSet)
router.register(r'blogs/(?P<blog_id>[0-9]+)/posts/(?P<post_id>[0-9]+)/reply', PostViewSet)
router.register(r'blogs/(?P<blog_id>[0-9]+)/posts', PostViewSet)


urlpatterns = [
    url(r'^$', PostsListView.as_view()),
    url(r'^login/$', do_login),
    url(r'^logout/$', do_logout),
    url(r'^signup/$', RegisterView.as_view(success_url="/")),
    url(r'^blogs/$', BlogsListView.as_view()),
    url(r'^new-post/$', PostCreation.as_view()),
    url(r'^blogs/(?P<username>[0-9a-z]+)/$', PostsListView.as_view()),
    url(r'^blogs/(?P<owner>[0-9a-z]+)/(?P<pk>[0-9]+)$', PostDetailView.as_view(), name="posts_detail"),
    url(r'^starlord/', admin.site.urls),
    url(r'^api/1.0/', include(router.urls)),
    url(r'^api/1.0/image/', ImageUploadView.as_view()),
]

