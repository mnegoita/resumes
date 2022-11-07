from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout



# Logout view
def logout_view(request):
    """ Log user out. """
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))

  

