from django.urls import path 
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'resumes'


urlpatterns = [
    path('companies/', login_required(views.CompanyList.as_view()), name='company_list'),
    path('companies/add/', login_required(views.CompanyCreate.as_view()), name='company_add'),
    path('companies/search-results/', views.CompanySearchResults.as_view(), name="company_search"),
    path('companies/<int:pk>/', login_required(views.CompanyDetail.as_view()), name='company'),
    path('companies/<int:pk>/edit/', login_required(views.CompanyEdit.as_view()), name='company_edit'),
    path('companies/<int:pk>/delete/', login_required(views.CompanyDelete.as_view()), name='company_delete'),

    path('resumes/', login_required(views.ResumeList.as_view()), name='resume_list'),
    path('resumes/add/', login_required(views.ResumeCreate.as_view()), name='resume_add'),
    path('resumes/search-results/', login_required(views.ResumeSearchResults.as_view()), name="resume_search"),
    path('resumes/<int:pk>/', login_required(views.ResumeDetail.as_view()), name='resume'),
    path('resumes/<int:pk>/edit/', login_required(views.ResumeEdit.as_view()), name='resume_edit'),
    path('resumes/<int:pk>/delete/', login_required(views.ResumeDelete.as_view()), name='resume_delete'),

    path('jobpositions/', login_required(views.JobPositionList.as_view()), name='jobposition_list'),
    path('jobpositions/add/', login_required(views.JobPositionCreate.as_view()), name='jobposition_add'),
    path('jobpositions/search-results/', login_required(views.JobPositionSearchResults.as_view()), name="jobposition_search"),
    path('jobpositions/<int:pk>/', login_required(views.JobPositionDetail.as_view()), name='jobposition'),
    path('jobpositions/<int:pk>/edit/', login_required(views.JobPositionEdit.as_view()), name='jobposition_edit'),
    path('jobpositions/<int:pk>/delete/', login_required(views.JobPositionDelete.as_view()), name='jobposition_delete'),

    path('interviews/', login_required(views.InterviewList.as_view()), name='interview_list'),
    path('interviews/add/', login_required(views.InterviewCreate.as_view()), name='interview_add'),
    path('interviews/search-results/', login_required(views.InterviewSearchResults.as_view()), name="interview_search"),
    path('interviews/<int:pk>/', login_required(views.InterviewDetail.as_view()), name='interview'),
    path('interviews/<int:pk>/edit/', login_required(views.InterviewEdit.as_view()), name='interview_edit'),
    path('interviews/<int:pk>/delete/', login_required(views.InterviewDelete.as_view()), name='interview_delete'),

    path('locations/', login_required(views.LocationList.as_view()), name='location_list'),
    path('locations/add/', login_required(views.LocationCreate.as_view()), name='location_add'),
    path('locations/search-results/', login_required(views.LocationSearchResults.as_view()), name="location_search"),
    path('locations/<int:pk>/', login_required(views.LocationDetail.as_view()), name='location'),
    path('locations/<int:pk>/edit/', login_required(views.LocationEdit.as_view()), name='location_edit'),
    path('locations/<int:pk>/delete/', login_required(views.LocationDelete.as_view()), name='location_delete'),

    path('jobtypes/', login_required(views.JobTypeList.as_view()), name='jobtype_list'),
    path('jobtypes/add/', login_required(views.JobTypeCreate.as_view()), name='jobtype_add'),
    path('jobtypes/search-results/', login_required(views.JobTypeSearchResults.as_view()), name="jobtype_search"),
    path('jobtypes/<int:pk>/', login_required(views.JobTypeDetail.as_view()), name='jobtype'),
    path('jobtypes/<int:pk>/edit/', login_required(views.JobTypeEdit.as_view()), name='jobtype_edit'),
    path('jobtypes/<int:pk>/delete/', login_required(views.JobTypeDelete.as_view()), name='jobtype_delete'),
    
]

