from django import forms 
from django.core.exceptions import ValidationError

from tempus_dominus.widgets import DatePicker, DateTimePicker

from .models import Company, Resume, JobPosition, Interview, Location, JobType, COUNTRY_CHOICES

from base.models import Category, Tag
from base.widgets import RelatedFieldWidgetSingle, RelatedFieldWidgetMultiple




# Company Form ######################################################################

class CompanyForm(forms.ModelForm):
    
    category = forms.ModelChoiceField(  
        required=False, 
        queryset=Category.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            Category, 
            related_url="base:category_add", 
            attrs={'class': 'select2-resumes form-control',
                   'style': 'width:90%'}
            )
        )
    
    tags = forms.ModelMultipleChoiceField(
        required=False, 
        queryset=Tag.objects.all(), 
        widget=RelatedFieldWidgetMultiple(
            Tag, 
            related_url="base:tag_add", 
            attrs={'class': 'select2-resumes form-control' ,
                   'style': 'width:90%'}
            )
        )


    class Meta:
        model = Company

        fields = ['name', 'website', 'info', 'category', 'tags',  'files',]
        widgets = {	      
          'name': forms.TextInput(attrs={'class': 'form-control'}),
          'website': forms.TextInput(attrs={'class': 'form-control'}),
          'info': forms.Textarea(attrs={'class': 'form-control', 'style': 'border: none', }),
          'files': forms.ClearableFileInput(attrs={'multiple': True}),
        }


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(author=self.user)
        self.fields['tags'].queryset = Tag.objects.filter(author=self.user)


    def full_clean(self):
        super().full_clean()
       
        company_name = self.instance.name

        msg = f"You already added {company_name}"

        try:
            self.instance.validate_unique()
        except ValidationError:
            self._update_errors(msg)


# Resume Form ######################################################################

class ResumeForm(forms.ModelForm):
    
    category = forms.ModelChoiceField(
        required=False, 
        queryset=Category.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            Category, 
            related_url="base:category_add", 
            attrs={'class': 'select2-resumes form-control',
                   'style': 'width:90%'}
            )
        )
    
    tags = forms.ModelMultipleChoiceField(
        required=False, 
        queryset=Tag.objects.all(), 
        widget=RelatedFieldWidgetMultiple(
            Tag, 
            related_url="base:tag_add", 
            attrs={'class': 'select2-resumes form-control' ,
                   'style': 'width:90%'}
            )
        )

    date_created = forms.DateField(
        widget=DatePicker(attrs={'class': 'form-control'}))

    class Meta:
        model = Resume
        fields = ['title', 'description', 'date_created', 'category', 'tags',  'content', 'files']
        widgets = {	      
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'style': 'border: none', }),
            'files': forms.ClearableFileInput(attrs={'multiple': True, }),
       }


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(author=self.user)
        self.fields['tags'].queryset = Tag.objects.filter(author=self.user)


    def full_clean(self):
        super().full_clean()
       
        resume_title = self.instance.title

        msg = f"You already added a resume with title {resume_title}"

        try:
            self.instance.validate_unique()
        except ValidationError:
            self._update_errors(msg)


# Job Position Form ######################################################################

class JobPositionForm(forms.ModelForm):

    location = forms.ModelChoiceField(
        required=True, 
        queryset=Location.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            Location, 
            related_url="resumes:location_add",  
            attrs={'class': 'select2-resumes form-control',
            'style': 'width:90%'}, 
            )
        )

    company = forms.ModelChoiceField(
        required=True, 
        queryset=Company.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            Company, 
            related_url="resumes:company_add", 
            attrs={'class': 'select2-resumes form-control',
            'style': 'width:90%'}, 
            )
        )

    job_type = forms.ModelChoiceField(
        required=False, 
        queryset=JobType.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            JobType, 
            related_url="resumes:jobtype_add", 
            attrs={'class': 'select2-resumes form-control',
            'style': 'width:90%'}, 
            )
        )

    resume_sent = forms.ModelChoiceField(
        required=False, 
        queryset=Resume.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            Resume, 
            related_url="resumes:resume_add",  
            attrs={'class': 'select2-resumes form-control',
            'style': 'width:90%'}, 
            )
        )
    
    category = forms.ModelChoiceField(
        required=False, 
        queryset=Category.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            Category, 
            related_url="base:category_add", 
            attrs={'class': 'select2-resumes form-control',
                   'style': 'width:90%'}
            )
        )
    
    tags = forms.ModelMultipleChoiceField(
        required=False, 
        queryset=Tag.objects.all(), 
        widget=RelatedFieldWidgetMultiple(
            Tag, 
            related_url="base:tag_add", 
            attrs={'class': 'select2-resumes form-control' ,
                   'style': 'width:90%'}
            )
        )  

    date_found = forms.DateField(
        required=False, 
        widget=DatePicker(attrs={'class': 'form-control'}))

    date_applied = forms.DateField(
        required=False, 
        widget=DatePicker(attrs={'class': 'form-control'}))
    

    class Meta:
        model = JobPosition
        fields = ['title', 
                  'location',
                  'company', 
                  'job_type',
                  'salary',
                  'date_found',  
                  'date_applied', 
                  'resume_sent', 
                  'category', 
                  'tags',                  
                  'content', 
                  ]
        widgets = {
	      
          'title': forms.TextInput(attrs={'class': 'form-control'}),
          'salary': forms.TextInput(attrs={'class': 'form-control'}),
          'content': forms.Textarea(attrs={'class': 'form-control', 'style': 'border: none', }), 
       }


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(author=self.user)
        self.fields['location'].queryset = Location.objects.filter(author=self.user)
        self.fields['job_type'].queryset = JobType.objects.filter(author=self.user)
        self.fields['resume_sent'].queryset = Resume.objects.filter(author=self.user)
        self.fields['category'].queryset = Category.objects.filter(author=self.user)
        self.fields['tags'].queryset = Tag.objects.filter(author=self.user)


# Interview Form ######################################################################

class InterviewForm(forms.ModelForm):
    
    job_position = forms.ModelChoiceField(
        required=True, 
        queryset=JobPosition.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            JobPosition, 
            related_url="resumes:jobposition_add", 
            attrs={'class': 'select2-resumes',
            'style': 'width:90%'} 
            )
        )

    date_sch = forms.DateTimeField(
        required=True, 
        widget=DateTimePicker(attrs={'class': 'form-control'}))

    resume = forms.ModelChoiceField(
        required=True, 
        queryset=Resume.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            Resume, 
            related_url="resumes:resume_add", 
            attrs={'class': 'select2-resumes',
            'style': 'width:90%'}
            )
        )

    category = forms.ModelChoiceField(
        required=False, 
        queryset=Category.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            Category, 
            related_url="base:category_add", 
            attrs={'class': 'select2-resumes form-control',
                   'style': 'width:90%'}
            )
        )
    
    tags = forms.ModelMultipleChoiceField(
        required=False, 
        queryset=Tag.objects.all(), 
        widget=RelatedFieldWidgetMultiple(
            Tag, 
            related_url="base:tag_add", 
            attrs={'class': 'select2-resumes form-control' ,
                   'style': 'width:90%'}
            )
        )
  

    class Meta:
        model = Interview
        fields = ['title', 'job_position', 'date_sch', 'resume', 'category', 'tags',  'notes',]
        widgets = {	      
          'title': forms.TextInput(attrs={'class': 'form-control'}),
          'notes': forms.Textarea(attrs={'class': 'form-control', 'style': 'border: none', }), 
       }


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields['job_position'].queryset = JobPosition.objects.filter(author=self.user)
        self.fields['resume'].queryset = Resume.objects.filter(author=self.user)
        self.fields['category'].queryset = Category.objects.filter(author=self.user)
        self.fields['tags'].queryset = Tag.objects.filter(author=self.user)

    
    def full_clean(self):
        super().full_clean()
       
        interview_title = self.instance.title

        msg = f"You already added an interview with title {interview_title}"

        try:
            self.instance.validate_unique()
        except ValidationError:
            self._update_errors(msg)


# Location Form ###########################################################################################

class LocationForm(forms.ModelForm):

    city = forms.CharField(
        required=True,
        label="city",
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )

    prov_st = forms.CharField(
        label="prov_st",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )

    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        required=True,
        widget = forms.Select(attrs={'class': 'select2-resumes form-control'},) 
    )  

    class Meta:
        model = Location
        fields = ['city', 'prov_st', 'country']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def full_clean(self):
        super().full_clean()
       
        loc_city = self.instance.city
        loc_prov_st = self.instance.prov_st
        loc_country = self.instance.country
        
        msg = f"You already added {loc_city} {loc_prov_st}, {loc_country}"

        try:
            self.instance.validate_unique()
        except ValidationError:
            self._update_errors(msg)


# JobType Form ####################################################################################

class JobTypeForm(forms.ModelForm):

    job_type = forms.CharField(
        label="job_type",
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )

    class Meta:
        model = JobType
        fields = ['job_type', ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def full_clean(self):
        super().full_clean()
       
        job_type = self.instance.job_type

        msg = f"You already added this {job_type} job type"

        try:
            self.instance.validate_unique()
        except ValidationError:
            self._update_errors(msg)


