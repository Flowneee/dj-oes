from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy

from . import models


class RegisterView(CreateView):
    model = models.User
    template_name = 'users/register.html'
    success_url = reverse_lazy('index')
