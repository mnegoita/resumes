from django import forms 
from django.core.exceptions import ValidationError
from .models import Category, Tag




# CategoryForm #################################################################

class CategoryForm(forms.ModelForm):

    name = forms.CharField(
        label="name",
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )

    slug = forms.CharField(
        label="slug",
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )

  
    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent',] 

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def full_clean(self):
        super().full_clean()
       
        category_name = self.instance.name

        msg = f"Yuou already added {category_name} category"

        try:
            self.instance.validate_unique()
        except ValidationError:
            self._update_errors(msg)


# TagForm #################################################################

class TagForm(forms.ModelForm):

    name = forms.CharField(
        label="name",
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )

    slug = forms.CharField(
        label="slug",
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
	  
    class Meta:
        model = Tag
        fields = ['name', 'slug',]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def full_clean(self):
        super().full_clean()
       
        tag_name = self.instance.name

        msg = f"Yuou already added {tag_name} tag"

        try:
            self.instance.validate_unique()
        except ValidationError:
            self._update_errors(msg)


# SearchForm #################################################################

OBJ_TYPE_CHOICES = (
    ('', 'All Objects'),
    ('category', 'Categories'),
    ('tag', 'Tags'),
    ('Resumes', (
        ('jobposition', 'Job Position'),
        ('resume', 'Resume'),
        ('interview', 'Interview'),
        ('company', 'Company'),
        ('location', 'Location'),
        ('jobtype', 'Job Type'),
    )),
)

class SearchForm(forms.Form):    
    q = forms.CharField(
            label='Search', 
            widget=forms.TextInput(attrs={'class': 'form-control', })
        )
    obj_type = forms.ChoiceField(
            choices=OBJ_TYPE_CHOICES, 
            required=False, 
            label='Type',
            widget = forms.Select(attrs = {'class': 'form-control'})
        )




