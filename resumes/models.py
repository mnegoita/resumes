from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import os
from ckeditor_uploader.fields import RichTextUploadingField

from base.models import Category, Tag 



# Company model ######################################################################################

def companies_upload_path(instance, filename):
    return 'companies/{0}/{1}/{2}'.format(instance.author, instance.name, filename)


class Company(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True, default="")      
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)    
    files = models.FileField(upload_to=companies_upload_path, blank=True) 
    info = RichTextUploadingField(blank=True, null=True, default="") 
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def file_link(self):
        if self.files:
            return '<a href="{0}" target="_blank">{1}</a>'.format(self.files.url, os.path.basename(self.files.name), )
        else:
            return '<span class="text-muted">&mdash;</span>'

    def get_absolute_url(self):
        return "/companies/{0}/".format(self.id)

    def __str__(self):
        return self.name   

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = 'Companies'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields = ['author', 'name',],
                name = 'company_unique_author_name'
            )
        ]


# Resume model ######################################################################################

def resumes_upload_path(instance, filename):
    return 'resumes/{0}/{1}/{2}'.format(instance.author, instance.title, filename)


class Resume(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=90, blank=True, default="")       
    date_created = models.DateField(blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)    
    content = RichTextUploadingField()
    files = models.FileField(upload_to=resumes_upload_path, blank=True) 
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    clone_fields = [
                    'title',
                    'description',
                    'content',
                    ]

    def file_link(self):
        if self.files:
            return '<a href="{0}" target="_blank">{1}</a>'.format(self.files.url, os.path.basename(self.files.name), )
        else:
            return '<span class="text-muted">&mdash;</span>'

    def get_absolute_url(self):
        return "/resumes/{0}/".format(self.id)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Resume"
        verbose_name_plural = 'Resumes'
        ordering = ['title']
        constraints = [
            models.UniqueConstraint(
                fields = ['author', 'title',],
                name = 'resume_unique_author_title'
            )
        ]


# Location model ######################################################################################

COUNTRy_1 = 'Canada'
COUNTRY_2 = 'US'

COUNTRY_CHOICES = [
    (COUNTRy_1, 'Canada'),
    (COUNTRY_2, 'US'),
]

class Location(models.Model):
    city = models.CharField(max_length=200)
    prov_st = models.CharField(max_length=2, verbose_name = "Province/State")
    country = models.CharField(
        max_length=20,
        choices = COUNTRY_CHOICES,
        default = COUNTRy_1)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return "/locations/{0}/".format(self.id)

    def __str__(self):
        return "{0}, {1}, {2}".format(str(self.city), str(self.prov_st), str(self.country))

    def save(self):
        self.prov_st = self.prov_st.upper()
        super().save()

    class Meta:
        verbose_name_plural = 'Locations'
        ordering = ['city']
        constraints = [
            models.UniqueConstraint(
                fields = ['author', 'city', 'prov_st', 'country'],
                name = 'unique_author_city_prov_st_country'
            )
        ]


# Job Type model ######################################################################################

class JobType(models.Model):
    job_type = models.CharField(max_length=40)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return "/jobtypes/{0}/".format(self.id)

    def __str__(self):
        return self.job_type

    class Meta:
        verbose_name = "Job Type"
        verbose_name_plural = 'Job Types'
        ordering = ['job_type']
        constraints = [
            models.UniqueConstraint(
                fields = ['author', 'job_type',],
                name = 'unique_author_job_type'
            )
        ]


# Job Position model ######################################################################################

class JobPosition(models.Model):
    title = models.CharField(max_length=200)
    company = models.ForeignKey(Company, related_name = 'jobpositions', on_delete=models.PROTECT)
    location = models.ForeignKey(Location, related_name = 'jobpositions', on_delete=models.PROTECT)
    job_type = models.ForeignKey(JobType, related_name = 'jobpositions', on_delete=models.PROTECT,
                                 verbose_name = "Job Type")
    salary = models.CharField(max_length=80, blank=True, default="") 
    date_found = models.DateField(blank=True, null=True) 
    date_applied = models.DateField(blank=True, null=True, default=None)
    resume_sent = models.ForeignKey(
        Resume, 
        blank=True, 
        null=True, 
        related_name = 'jobpositions', 
        on_delete = models.PROTECT)        
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)   
    tags = models.ManyToManyField(Tag, blank=True)
    content = RichTextUploadingField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return "/jobpositions/{0}/".format(self.id)

    def __str__(self):
        return "{0} ({1})".format(str(self.title), str(self.company))

    def save(self):
        if not self.date_found:
            self.date_found = timezone.now()
        super(JobPosition, self).save()

    class Meta:
        verbose_name = "Job Position"
        verbose_name_plural = 'Job Positions'
        ordering = ['-date_found']


# Interview model ######################################################################################

class Interview(models.Model):
    title = models.CharField(max_length=255)    
    job_position = models.ForeignKey(JobPosition, on_delete=models.PROTECT)
    date_sch = models.DateTimeField(verbose_name="Date Scheduled")
    resume = models.ForeignKey(Resume, on_delete=models.PROTECT)   
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)    
    notes = RichTextUploadingField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return "/interviews/{0}/".format(self.id)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Interview"
        verbose_name_plural = 'Interviews'
        ordering = ['title']
        constraints = [
            models.UniqueConstraint(
                fields = ['author', 'title',],
                name = 'interview_unique_author_title'
            )
        ]

