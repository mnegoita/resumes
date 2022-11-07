# Generated by Django 4.1.2 on 2022-11-06 21:26

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import resumes.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('website', models.URLField(blank=True, default='')),
                ('files', models.FileField(blank=True, upload_to=resumes.models.companies_upload_path)),
                ('info', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.category')),
                ('tags', models.ManyToManyField(blank=True, to='base.tag')),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, default='', max_length=90)),
                ('date_created', models.DateField(blank=True, null=True)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('files', models.FileField(blank=True, upload_to=resumes.models.resumes_upload_path)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.category')),
                ('tags', models.ManyToManyField(blank=True, to='base.tag')),
            ],
            options={
                'verbose_name': 'Resume',
                'verbose_name_plural': 'Resumes',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=200)),
                ('prov_st', models.CharField(max_length=2, verbose_name='Province/State')),
                ('country', models.CharField(choices=[('Canada', 'Canada'), ('US', 'US')], default='Canada', max_length=20)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Locations',
                'ordering': ['city'],
            },
        ),
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_type', models.CharField(max_length=40)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Job Type',
                'verbose_name_plural': 'Job Types',
                'ordering': ['job_type'],
            },
        ),
        migrations.CreateModel(
            name='JobPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('salary', models.CharField(blank=True, default='', max_length=80)),
                ('date_found', models.DateField(blank=True, null=True)),
                ('date_applied', models.DateField(blank=True, default=None, null=True)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.category')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='jobpositions', to='resumes.company')),
                ('job_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='jobpositions', to='resumes.jobtype', verbose_name='Job Type')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='jobpositions', to='resumes.location')),
                ('resume_sent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='jobpositions', to='resumes.resume')),
                ('tags', models.ManyToManyField(blank=True, to='base.tag')),
            ],
            options={
                'verbose_name': 'Job Position',
                'verbose_name_plural': 'Job Positions',
                'ordering': ['-date_found'],
            },
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('date_sch', models.DateTimeField(verbose_name='Date Scheduled')),
                ('notes', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.category')),
                ('job_position', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='resumes.jobposition')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='resumes.resume')),
                ('tags', models.ManyToManyField(blank=True, to='base.tag')),
            ],
            options={
                'verbose_name': 'Interview',
                'verbose_name_plural': 'Interviews',
                'ordering': ['title'],
            },
        ),
        migrations.AddConstraint(
            model_name='resume',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='resume_unique_author_title'),
        ),
        migrations.AddConstraint(
            model_name='location',
            constraint=models.UniqueConstraint(fields=('author', 'city', 'prov_st', 'country'), name='unique_author_city_prov_st_country'),
        ),
        migrations.AddConstraint(
            model_name='jobtype',
            constraint=models.UniqueConstraint(fields=('author', 'job_type'), name='unique_author_job_type'),
        ),
        migrations.AddConstraint(
            model_name='interview',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='interview_unique_author_title'),
        ),
        migrations.AddConstraint(
            model_name='company',
            constraint=models.UniqueConstraint(fields=('author', 'name'), name='company_unique_author_name'),
        ),
    ]
