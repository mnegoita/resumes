from django import template
from django.urls import reverse

register = template.Library()

template_path = 'base/buttons/'




def get_view_name(instance, action):
    """
    Function to get the name of a specific when using the same pattern in forming
    the name of the views.
    Used for views like: add, edit, delete, list, etc
    """

    assert action in ('add', 'edit', 'delete', 'list')
    view_name = "{}:{}_{}".format(
        instance._meta.app_label, instance._meta.model_name, action
    )
    
    return view_name


# Add Button ##########################################

@register.inclusion_tag(template_path + 'add.html')
def add_button(app_name, obj_name):

    add_url = reverse(f"{app_name}:{obj_name}_add")

    return {
        'url': add_url,
    }


# List View URL template tag ##########################
# Used in breadcrumb

@register.simple_tag
def list_view_url(instance):
    
    view_name = get_view_name(instance, 'list')    
    url = '{}'.format(reverse(view_name))

    return url
    

# Edit Button ############################################

@register.inclusion_tag(template_path + 'edit.html')
def edit_button(instance):
    view_name = get_view_name(instance, 'edit')

    if hasattr(instance, 'slug'):
        kwargs = {'slug': instance.slug}
    else:
        kwargs = {'pk': instance.pk}

    url = reverse(view_name, kwargs=kwargs)

    return {
        'url': url,
    }


# Delete Button #############################################

@register.inclusion_tag(template_path + 'delete.html')
def delete_button(instance, use_pk=False):
    view_name = get_view_name(instance, 'delete')

    if hasattr(instance, 'slug') and not use_pk:
        kwargs = {'slug': instance.slug}
    else:
        kwargs = {'pk': instance.pk}

    url = reverse(view_name, kwargs=kwargs)

    return {
        'url': url,
    }




