from rest_framework.filters import SearchFilter

from blogs.models import Blog, Post


class BlogFilter(SearchFilter):

    def filter_queryset(self, request, queryset, view):
        search_fields = getattr(view, 'search_fields', None)
        search_terms = self.get_search_terms(request)

        if not search_fields or not search_terms:
            return queryset

        queryset = queryset.filter(posts__in=Post.objects.filter(title__icontains='Title'))

        return queryset