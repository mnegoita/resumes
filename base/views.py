from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.utils.html import escape, escapejs
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django_tables2 import RequestConfig
from collections import OrderedDict

# Base Imports
from .models import Category, Tag
from .tables import CategoryTable, TagTable
from .filters import CategoryFilter, TagFilter
from .forms import CategoryForm, TagForm, SearchForm

# Resumes imports
from resumes.models import Company, Resume, JobPosition, Interview, Location, JobType
from resumes.tables import CompanyTable, ResumeTable, JobPositionTable, InterviewTable, LocationTable, JobTypeTable
from resumes.filters import CompanyFilter, ResumeFilter, JobPositionFilter, InterviewFilter, LocationFilter, JobTypeFilter


template_path = 'base/'
search_results_template = "base/search_results.html"
confirm_delete_template = "base/form_confirm_delete.html"



# Base Views ########################################################

class BaseItemsList(ListView):
    """
    Base class view used to display the items as list or as boxes
    Subclassing ListView to make use of pagination.
    As template, it can use the template which displays the items as boxes
    or a template which displays the items as a list of links.
    """
    model = None
    template_name = template_path + 'base_items_list_boxes.html'

    
    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Getting the object name, lower, and with spaces between words removed 
        # so it can be used with add button templatetag
        # Also getting the app name to use it in the add button templatetag
        context['obj_name'] = self.model._meta.verbose_name.lower().replace(" ", "")
        context['app_name'] = self.model._meta.app_label
        context['model'] = self.model

        return context


class BaseItemsSearchResults(View):
    """
    Base class view used to display the search results 
    as tables using django-tables2.
    The queyset is filtered by the logged in user
    """
    queryset = None
    table = None
    filter = None
    template_name = template_path + "base_search_results.html"


    def get(self, request):
        
        queryset = self.queryset.filter(author=request.user)   

        if self.filter:
            queryset = self.filter(request.GET, queryset).qs

        table = self.table(queryset, orderable=False)
        
        paginate = {'paginator_class': Paginator, 'per_page': 15}
        RequestConfig(request, paginate).configure(table)
                
        return render(request, self.template_name, {
            'table': table,
            'model': self.queryset.model,
        }) 


class BaseItemCreateWithPopup(CreateView):
    """
    Base class view used for item creation with popup window.
    This is for those items that are ForeigKey for a model and can be created from 
    a popup window in the specific model
    """
    model = None
    form_class = None
    template_name = None
    template_name_popup = None
    cancel_button_url = None


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        kwargs['instance'] = self.model(author=self.request.user)

        return kwargs
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user   
        self.object.save()

        return super().form_valid(form)  
      
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_type'] = self.model._meta.verbose_name
        context['cancel_button_url'] = self.cancel_button_url

        if ('_popup' in self.request.GET):
            self.template_name = self.template_name_popup
            context['popup'] = self.request.GET['_popup'] 
        return context

      
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if "_popup" in request.POST:
            if self.object: 
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                    (escape(self.object.pk), escapejs(self.object)))

        return response


class BaseItemEdit(UpdateView):
    """
    Base class view used for item editiong
    """
    model = None
    form_class = None
    template_name = None


    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_type'] = self.model._meta.verbose_name
        return context


# Home Page View ###############################################################################

class HomePage(View):
    template_name = template_path + 'home.html'


    def get(self, request):

        user_jobpositions = JobPosition.objects.filter(author=self.request.user).count()
        user_resumes = Resume.objects.filter(author=self.request.user).count()
        user_interviews = Interview.objects.filter(author=self.request.user).count()
        user_companies = Company.objects.filter(author=self.request.user).count()
        user_jobtypes = JobType.objects.filter(author=self.request.user).count()
        user_locations = Location.objects.filter(author=self.request.user).count()


        return render(request, self.template_name, {
            'user_jobpositions': user_jobpositions,
            'user_resumes': user_resumes,
            'user_interviews': user_interviews,
            'user_companies': user_companies,
            'user_jobtypes': user_jobtypes,
            'user_locations': user_locations,
        })


# Errors Views ################################################################################

def custom_page_not_found_view(request, exception):
    return render(request, "base/errors/404.html", {})

def custom_error_view(request, exception=None):
    return render(request, "base/errors/500.html", {})

def custom_permission_denied_view(request, exception=None):
    return render(request, "base/errors/403.html", {})

def custom_bad_request_view(request, exception=None):
    return render(request, "base/errors/400.html", {})


# Category Views ###############################################################################

class CategoryList(BaseItemsList):
    model = Category
    template_name = template_path + "category_list.html"
    paginate_by = 18
    

class CategorySearchResults(BaseItemsSearchResults):
    queryset = Category.objects.all()
    table = CategoryTable
    filter = CategoryFilter


class CategoryDetail(DetailView):
    model = Category
    template_name = template_path + 'category_detail.html'

    def get(self, request, hierarchy=None, **kwargs):
        
        category_slug = hierarchy.split('/')
        parent = None
        root = Category.objects.filter(author=self.request.user)

        for slug in category_slug[:-1]:
            parent = root.get(parent=parent, slug = slug)

        try:
            instance = Category.objects.get(author=self.request.user, parent=parent, slug=category_slug[-1])

            cat_jobpositions = instance.jobposition_set.all()
            paginator = Paginator(cat_jobpositions, 5)
            page = self.request.GET.get('page1')
            try:
                cat_jobpositions = paginator.page(page)
            except PageNotAnInteger:
                cat_jobpositions = paginator.page(1)
            except EmptyPage:
                cat_jobpositions = paginator.page(paginator.num_pages)
                
            cat_resumes = instance.resume_set.all()
            paginator = Paginator(cat_resumes, 5)
            page = self.request.GET.get('page2')
            try:
                cat_resumes = paginator.page(page)
            except PageNotAnInteger:
                cat_resumes = paginator.page(1)
            except EmptyPage:
                cat_resumes = paginator.page(paginator.num_pages)

            cat_interviews = instance.interview_set.all()
            paginator = Paginator(cat_interviews, 5)
            page = self.request.GET.get('page3')
            try:
                cat_interviews = paginator.page(page)
            except PageNotAnInteger:
                cat_interviews = paginator.page(1)
            except EmptyPage:
                cat_interviews = paginator.page(paginator.num_pages)

            cat_companies = instance.company_set.all()
            paginator = Paginator(cat_companies, 5)
            page = self.request.GET.get('page4')
            try:
                cat_companies = paginator.page(page)
            except PageNotAnInteger:
                cat_companies = paginator.page(1)
            except EmptyPage:
                cat_companies = paginator.page(paginator.num_pages)

        except:
            instance = get_object_or_404(Category, slug = category_slug[-1])
            return render(request, self.template_name, {
                'instance':instance,
                })
        else:
            return render(request, self.template_name, {
                'instance': instance,
                'cat_jobpositions': cat_jobpositions,
                'cat_resumes': cat_resumes,
                'cat_interviews': cat_interviews,
                'cat_companies': cat_companies
                })


class CategoryCreate(BaseItemCreateWithPopup):
    model = Category
    form_class = CategoryForm
    template_name = template_path + "category_form.html"
    template_name_popup = template_path + "category_form_popup.html"
    cancel_button_url = reverse_lazy('base:category_list')


class CategoryEdit(BaseItemEdit):
    model = Category
    form_class = CategoryForm
    template_name = template_path + "category_form.html"


class CategoryDelete(DeleteView):
    model = Category
    success_url = reverse_lazy('base:category_list')
    template_name = confirm_delete_template


# Tag Views ############################################################################################

class TagList(BaseItemsList):
    model = Tag
    paginate_by = 18


class TagSearchResults(BaseItemsSearchResults):
    queryset = Tag.objects.all()
    table = TagTable
    filter = TagFilter


class TagDetail(DetailView):
    model = Tag
    template_name = template_path + 'tag_detail.html'

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['obj_type'] = self.model._meta.verbose_name
        
        tag_jobpositions = self.object.jobposition_set.all()
        paginator = Paginator(tag_jobpositions, 5)
        page = self.request.GET.get('page1')
        try:
            tag_jobpositions = paginator.page(page)
        except PageNotAnInteger:
            tag_jobpositions = paginator.page(1)
        except EmptyPage:
            tag_jobpositions = paginator.page(paginator.num_pages)

        tag_resumes = self.object.resume_set.all()
        paginator = Paginator(tag_resumes, 5)
        page = self.request.GET.get('page2')
        try:
            tag_resumes = paginator.page(page)
        except PageNotAnInteger:
            tag_resumes = paginator.page(1)
        except EmptyPage:
            tag_resumes = paginator.page(paginator.num_pages)

        tag_interviews = self.object.interview_set.all()
        paginator = Paginator(tag_interviews, 5)
        page = self.request.GET.get('page3')
        try:
            tag_interviews = paginator.page(page)
        except PageNotAnInteger:
            tag_interviews = paginator.page(1)
        except EmptyPage:
            tag_interviews = paginator.page(paginator.num_pages)

        tag_companies = self.object.company_set.all()
        paginator = Paginator(tag_companies, 5)
        page = self.request.GET.get('page4')
        try:
            tag_companies = paginator.page(page)
        except PageNotAnInteger:
            tag_companies = paginator.page(1)
        except EmptyPage:
            tag_companies = paginator.page(paginator.num_pages)

        context['tag_jobpositions'] = tag_jobpositions
        context['tag_resumes'] = tag_resumes
        context['tag_interviews'] = tag_interviews
        context['tag_companies'] = tag_companies

        return context


class TagCreate(BaseItemCreateWithPopup):
    model = Tag
    form_class = TagForm
    template_name = template_path + "tag_form.html"
    template_name_popup = template_path + "tag_form_popup.html"
    cancel_button_url = reverse_lazy('base:tag_list')


class TagEdit(BaseItemEdit):
    model = Tag
    form_class = TagForm
    template_name = template_path + "tag_form.html"


class TagDelete(DeleteView):
    model = Tag
    success_url = reverse_lazy('base:tag_list')
    template_name = confirm_delete_template


# SearchView #############################################################

class SearchView(View):
    template_name = template_path + 'search/search.html'

    def get(self, request):

        SEARCH_TYPES = OrderedDict((
            ('category', {
                    'queryset': Category.objects.filter(author=self.request.user),
                    'filter': CategoryFilter,
                    'table': CategoryTable,
                    'url': 'base:category_search'
            }),
            ('tag', {
                    'queryset': Tag.objects.filter(author=self.request.user),
                    'filter': TagFilter,
                    'table': TagTable,
                    'url': 'base:tag_search'
            }),
            ('company', {
                    'queryset': Company.objects.filter(author=self.request.user).prefetch_related('category', 'tags',),
                    'filter': CompanyFilter,
                    'table': CompanyTable,
                    'url': 'resumes:company_search'
            }),
            ('resume', {
                    'queryset': Resume.objects.filter(author=self.request.user).prefetch_related('category', 'tags',),
                    'filter': ResumeFilter,
                    'table': ResumeTable,
                    'url': 'resumes:resume_search'
            }),
            ('jobposition', {
                    'queryset': JobPosition.objects.filter(author=self.request.user).prefetch_related('category', 
                                                                                                      'tags',
                                                                                                      'company',
                                                                                                      'location',
                                                                                                      'job_type',
                                                                                                      'resume_sent',
                                                                                                      ),
                    'filter': JobPositionFilter,
                    'table': JobPositionTable,
                    'url': 'resumes:jobposition_search'
            }),
            ('interview', {
                    'queryset': Interview.objects.filter(author=self.request.user).prefetch_related('category', 'tags',),
                    'filter': InterviewFilter,
                    'table': InterviewTable,
                    'url': 'resumes:interview_search'
            }),
            ('location', {
                    'queryset': Location.objects.filter(author=self.request.user),
                    'filter': LocationFilter,
                    'table': LocationTable,
                    'url': 'resumes:location_search'
            }),
            ('jobtype', {
                    'queryset': JobType.objects.filter(author=self.request.user),
                    'filter': JobTypeFilter,
                    'table': JobTypeTable,
                    'url': 'resumes:jobtype_search'
            }),
        ))

        # When no query
        if 'q' not in request.GET:
            return render(request, self.template_name, { 'form': SearchForm(), })

        form = SearchForm(request.GET)
        results = []

        if form.is_valid():

            if form.cleaned_data['obj_type']:
                obj_types = [form.cleaned_data['obj_type']]

            else:
                obj_types = SEARCH_TYPES.keys()

            for obj_type in obj_types:
                
                queryset = SEARCH_TYPES[obj_type]['queryset']
                filter_cls = SEARCH_TYPES[obj_type]['filter']
                table = SEARCH_TYPES[obj_type]['table']
                url = SEARCH_TYPES[obj_type]['url']

                filtered_queryset = filter_cls({'q': form.cleaned_data['q']}, queryset=queryset).qs
                table = table(filtered_queryset, orderable=False)

                table.paginate(per_page=10)
                if table.page:
                    results.append({
                        'name': queryset.model._meta.verbose_name_plural,
                        'table': table,
                        'url': '{}?q={}'.format(reverse(url), form.cleaned_data['q']),
                    })

        return render(request, self.template_name, {
            'form': form,
            'results': results,
        })
