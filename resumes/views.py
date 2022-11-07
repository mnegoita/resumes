from django.shortcuts import render
from django.views.generic import View, DetailView, CreateView, DeleteView
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models import ProtectedError
from django_tables2 import RequestConfig

from base.views import BaseItemsList, BaseItemsSearchResults, BaseItemCreateWithPopup, BaseItemEdit

from .models import Company, Resume, JobPosition, Interview, Location, JobType
from .tables import (
    CompanyTable, ResumeTable, JobPositionTable, InterviewTable, LocationTable, JobTypeTable
    )
from .filters import (CompanyFilter, ResumeFilter, JobPositionFilter, InterviewFilter, 
    LocationFilter, JobTypeFilter)
from .forms import (JobPositionForm, CompanyForm, ResumeForm, InterviewForm, 
    LocationForm,  JobTypeForm)

template_path = 'resumes/'
confirm_delete_template = "base/form_confirm_delete.html"




# Company Views ###################################################

class CompanyList(BaseItemsList):
    model = Company
    paginate_by = 18


class CompanySearchResults(BaseItemsSearchResults):
    queryset = Company.objects.all()
    table = CompanyTable
    filter = CompanyFilter


class CompanyDetail(DetailView):
    model = Company
    template_name = template_path + "company_detail.html"

    def get_queryset(self):
        return Company.objects.filter(author=self.request.user).prefetch_related('category', 'tags')

    def get_context_data(self, **kwargs):

        job_positions = JobPosition.objects.filter(
            author=self.request.user, 
            company=self.object.id).prefetch_related('company',
                                                    'location',
                                                    'job_type',
                                                    'resume_sent',)

        context = super().get_context_data(**kwargs)
        context['job_positions'] = job_positions
        context['model'] = self.model
        
        return context


class CompanyCreate(BaseItemCreateWithPopup):
    model = Company
    form_class = CompanyForm
    template_name = template_path + "company_form.html"
    template_name_popup = template_path + "company_form_popup.html"
    cancel_button_url = reverse_lazy('resumes:company_list')


class CompanyEdit(BaseItemEdit):
    model = Company
    form_class = CompanyForm
    template_name = template_path + "company_form.html"


class CompanyDelete(DeleteView):
    model = Company
    success_url = reverse_lazy('resumes:company_list')
    template_name = template_path + "company_confirm_delete.html"
    
    def get_queryset(self):
        return Company.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        job_positions = JobPosition.objects.filter(author=self.request.user, company=self.object.id)

        context = super().get_context_data(**kwargs)
        context['job_positions'] = job_positions
        context['obj_type'] = Company._meta.verbose_name
        
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            context = self.get_context_data(
                object=self.object,
                error="<strong> {0} </strong> cannot be deleted as the following items depend on it:".format(self.object.name)
            )
            return self.render_to_response(context) 
        return HttpResponseRedirect(success_url)


# Resume Views ##########################################################

class ResumeList(BaseItemsList):
    model = Resume
    paginate_by = 18


class ResumeSearchResults(BaseItemsSearchResults):
    queryset = Resume.objects.all()
    table = ResumeTable
    filter = ResumeFilter


class ResumeDetail(DetailView):
    model = Resume
    template_name = template_path + 'resume_detail.html'
    
    def get_queryset(self):
        return Resume.objects.filter(author=self.request.user).prefetch_related(
            "category",
            "tags",
        )

    def get_context_data(self, **kwargs):

        job_positions = JobPosition.objects.filter(
            author=self.request.user, 
            resume_sent=self.object.id).prefetch_related(
                'company',
                'location',
                'job_type',
                'resume_sent',)

        interviews = Interview.objects.filter(
            author=self.request.user,
            resume = self.object.id
        ).prefetch_related(
            'job_position',
            "resume",
            "category",
            "tags",
            )
        context = super().get_context_data(**kwargs)
        context['job_positions'] = job_positions
        context['interviews'] = interviews
        context['model'] = self.model
        
        return context


class ResumeCreate(BaseItemCreateWithPopup):
    model = Resume
    form_class = ResumeForm
    template_name = template_path + 'resume_form.html'
    template_name_popup = template_path + 'resume_form_popup.html'
    cancel_button_url = reverse_lazy('resumes:resume_list')


class ResumeEdit(BaseItemEdit):
    model = Resume
    form_class = ResumeForm
    template_name = template_path + 'resume_form.html'


class ResumeDelete(DeleteView):
    model = Resume
    success_url = reverse_lazy('resumes:resume_list')
    template_name = template_path + 'resume_confirm_delete.html'

    def get_queryset(self):
        return Resume.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        job_positions = JobPosition.objects.filter(author=self.request.user, resume_sent=self.object.id)
        interviews = Interview.objects.filter(author=self.request.user, resume=self.object.id)

        context = super().get_context_data(**kwargs)
        context['job_positions'] = job_positions
        context['interviews'] = interviews
        context['obj_type'] = self.model._meta.verbose_name
        
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            context = self.get_context_data(
                object=self.object,
                error="<strong> {0} </strong> cannot be deleted as the following items depend on it:".format(self.object.title)
            )
            return self.render_to_response(context) 
        return HttpResponseRedirect(success_url)


# Job Position Views ##################################################

class JobPositionList(View):
    model = JobPosition
    template_name = template_path + 'jobposition_list.html'
    filter = JobPositionFilter

    def get(self, request):
        self.queryset = self.model.objects.filter(author=request.user).prefetch_related(
            'company', 'location', 'job_type', 'resume_sent', )

        if self.filter:
            self.queryset = self.filter(request.GET, self.queryset).qs

        user_job_positions_ca = self.queryset.filter(location__country="Canada")
        user_job_positions_us = self.queryset.filter(location__country="US")

        obj_name = self.model._meta.verbose_name.lower().replace(" ", "")
        app_name = self.model._meta.app_label
        model = self.model
                
        return render(request, self.template_name, {

            'user_job_positions_ca': user_job_positions_ca,
            'user_job_positions_us': user_job_positions_us,

            'obj_name': obj_name,
            'app_name': app_name,
            'model': model,
        })

class JobPositionSearchResults(BaseItemsSearchResults):
    queryset = JobPosition.objects.all()
    table = JobPositionTable
    filter = JobPositionFilter


class JobPositionDetail(DetailView):
    model = JobPosition
    template_name = template_path + 'jobposition_detail.html'
    
    def get_queryset(self):
        return JobPosition.objects.filter(author=self.request.user)


class JobPositionCreate(BaseItemCreateWithPopup):
    model = JobPosition
    form_class = JobPositionForm
    template_name = template_path + 'jobposition_form.html'
    template_name_popup = template_path + 'jobposition_form_popup.html'
    cancel_button_url = reverse_lazy('resumes:jobposition_list')


class JobPositionEdit(BaseItemEdit):
    model = JobPosition
    form_class = JobPositionForm
    template_name = template_path + 'jobposition_form.html'


class JobPositionDelete(DeleteView):
    model = JobPosition
    success_url = reverse_lazy('resumes:jobposition_list')
    template_name = template_path + 'jobposition_confirm_delete.html'

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        interviews = Interview.objects.filter(author=self.request.user, job_position=self.object.id)
        
        context['interviews'] = interviews
        context['obj_type'] = JobPosition._meta.verbose_name
        
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            context = self.get_context_data(
                object=self.object,
                error="<strong> {0} </strong> cannot be deleted as the following items depend on it:".format(self.object.title)
            )
            return self.render_to_response(context) 
        return HttpResponseRedirect(success_url)
    

# Interview Views #############################################################################

class InterviewList(View):
    model = Interview
    template_name = template_path + 'interview_list.html'
    table = InterviewTable
    filter = InterviewFilter

    def get(self, request):
        self.queryset = self.model.objects.filter(author=request.user)

        if self.filter:
            self.queryset = self.filter(request.GET, self.queryset).qs

        table = self.table(self.queryset, orderable=False)

        paginate = {'paginator_class': Paginator, 'per_page': 15}
        RequestConfig(request, paginate).configure(table)

        obj_name = self.model._meta.verbose_name.lower().replace(" ", "")
        app_name = self.model._meta.app_label
                
        return render(request, self.template_name, {
            'queryset': self.queryset,
            'table': table,
            'obj_name': obj_name,
            'app_name': app_name,
            'model': self.model,
        })


class InterviewSearchResults(BaseItemsSearchResults):
    queryset = Interview.objects.all()
    table = InterviewTable
    filter = InterviewFilter


class InterviewDetail(DetailView):
    model = Interview
    template_name = template_path + 'interview_detail.html'
    
    def get_queryset(self):
        return Interview.objects.filter(author=self.request.user)


class InterviewCreate(CreateView):
    model = Interview
    form_class = InterviewForm
    template_name = template_path + 'interview_form.html'
    cancel_button_url = reverse_lazy('resumes:interview_list')


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
        return context          


class InterviewEdit(BaseItemEdit):
    model = Interview
    form_class = InterviewForm
    template_name = template_path + 'interview_form.html'


class InterviewDelete(DeleteView):
    model = Interview
    success_url = reverse_lazy('resumes:interview_list')
    template_name = confirm_delete_template

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)
        

# Location Views ##############################################

class LocationList(BaseItemsList):
    model = Location
    paginate_by = 18


class LocationSearchResults(BaseItemsSearchResults):
    queryset = Location.objects.all()
    table = LocationTable
    filter = LocationFilter


class LocationDetail(DetailView):
    model = Location
    template_name = template_path + 'location_detail.html'
    
    def get_queryset(self):
        return Location.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):

        job_positions = JobPosition.objects.filter(
            author=self.request.user, 
            location=self.object.id).prefetch_related('company',
                                                        'location',
                                                        'job_type',
                                                         'resume_sent',)

        context = super().get_context_data(**kwargs)
        context['job_positions'] = job_positions
        
        return context


class LocationCreate(BaseItemCreateWithPopup):
    model = Location
    form_class = LocationForm
    template_name = template_path + 'location_form.html'
    template_name_popup = template_path + 'location_form_popup.html'
    cancel_button_url = reverse_lazy('resumes:location_list')


class LocationEdit(BaseItemEdit):
    model = Location
    form_class = LocationForm
    template_name = template_path + 'location_form.html'


class LocationDelete(DeleteView):
    model = Location
    success_url = reverse_lazy('resumes:location_list')
    template_name = template_path + 'location_confirm_delete.html'

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        job_positions = JobPosition.objects.filter(author=self.request.user, location=self.object.id)

        context = super().get_context_data(**kwargs)
        context['job_positions'] = job_positions
        context['obj_type'] = Location._meta.verbose_name
        
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            context = self.get_context_data(
                object=self.object,
                error="<strong> {0}, {1}, {2} </strong> cannot be deleted as the following items depend on it:".format(self.object.city, self.object.prov_st, self.object.country, )
            )
            return self.render_to_response(context) 
        return HttpResponseRedirect(success_url)


# Job Type Views ##############################################

class JobTypeList(BaseItemsList):
    model = JobType
    paginate_by = 18


class JobTypeSearchResults(BaseItemsSearchResults):
    queryset = JobType.objects.all()
    table = JobTypeTable
    filter = JobTypeFilter


class JobTypeDetail(DetailView):
    model = JobType
    template_name = template_path + 'jobtype_detail.html'
    
    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):

        job_positions = JobPosition.objects.filter(
            author=self.request.user, 
            job_type=self.object.id).prefetch_related('company',
                                                    'location',
                                                    'job_type',
                                                    'resume_sent',)

        context = super().get_context_data(**kwargs)
        context['job_positions'] = job_positions
        
        return context


class JobTypeCreate(BaseItemCreateWithPopup):
    model = JobType
    form_class = JobTypeForm
    template_name = template_path + 'jobtype_form.html'
    template_name_popup = template_path + 'jobtype_form_popup.html'
    cancel_button_url = reverse_lazy('resumes:jobtype_list')


class JobTypeEdit(BaseItemEdit):
    model = JobType
    form_class = JobTypeForm
    template_name = template_path + 'jobtype_form.html'


class JobTypeDelete(DeleteView):
    model = JobType
    success_url = reverse_lazy('resumes:jobtype_list')
    template_name = template_path + 'jobtype_confirm_delete.html'

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        job_positions = JobPosition.objects.filter(author=self.request.user, job_type=self.object.id)

        context = super().get_context_data(**kwargs)
        context['job_positions'] = job_positions
        context['obj_type'] = JobType._meta.verbose_name
        
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            context = self.get_context_data(
                object=self.object,
                error="<strong> {0} </strong> cannot be deleted as the following items depend on it:".format(self.object.job_type)
            )
            return self.render_to_response(context) 
        return HttpResponseRedirect(success_url)



