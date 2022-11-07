import django_tables2 as tables

from base.tables import BaseTable
from .models import Company, Resume, JobPosition, Interview, Location, JobType




# Company Table ####################################################################################

class CompanyTable(BaseTable):
    name = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = Company
        fields = ('name', 'website', )


# Resume Table ####################################################################################

class ResumeTable(BaseTable):
    title = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = Resume
        fields = ('title', 'description', )


# Job Position Tables ####################################################################################

class JobPositionTable(BaseTable):
    title = tables.LinkColumn()
    company = tables.LinkColumn()
    location = tables.LinkColumn()
    job_type = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = JobPosition
        fields = ('title', 'company', 'location', 'job_type', 'salary', )


# Interview Table ####################################################################################

class InterviewTable(BaseTable):
    title = tables.LinkColumn()
    job_position = tables.LinkColumn()
    resume = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = Interview
        fields = ('title',  'job_position', 'resume',)


# Location Table ####################################################################################

class LocationTable(BaseTable):
    city = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = Location
        fields = ('city',  'prov_st', 'country')


# Job Type Table ####################################################################################

class JobTypeTable(BaseTable):
    job_type = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = JobType
        fields = ('job_type', )


