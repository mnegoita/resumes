import django_filters
from django.db.models import Q

from .models import Category, Tag



class CategoryFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = Category
        fields = ['name', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) ) 


class TagFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = Tag
        fields = ['name', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) ) 




