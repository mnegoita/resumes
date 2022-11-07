import django_filters
from django.db.models import Q

from .models import Company, Resume, JobPosition, Interview, Location, JobType




# Company Filter ######################################################################

class CompanyFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = Company
        fields = ['name', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) |
                               Q(info__icontains=value)
                               ) 


# Resume Filter ######################################################################

class ResumeFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = Resume
        fields = ['title', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(title__icontains=value) |
                               Q(description__icontains=value) |
                               Q(content__icontains=value)) 


# Job Position Filter ######################################################################

class JobPositionFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = JobPosition
        fields = ['title', 'content', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(title__icontains=value) |
                               Q(company__name__icontains=value) |
                               Q(location__city__icontains=value) |
                               Q(resume_sent__title__icontains=value) |
                               Q(content__icontains=value) 
                               ) 
	

# Interview Filter ######################################################################

class InterviewFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = Interview
        fields = ['title', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(title__icontains=value) | 
                               Q(job_position__title__icontains=value) |
                               Q(resume__title__icontains=value) |
                               Q(notes__icontains=value)
                               ) 


# Location Filter ######################################################################

class LocationFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = Location
        fields = ['city', 'prov_st', 'country', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(city__icontains=value) |
                               Q(prov_st__icontains=value) |
                               Q(country__icontains=value)) 


# Job Type Filter ######################################################################

class JobTypeFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = JobType
        fields = ['job_type',  ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(job_type__icontains=value) ) 


