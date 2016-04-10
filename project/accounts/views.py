from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import forms

from . import models


class UserRegistrationForm(forms.UserCreationForm):
    def __init__(self, *args, **kargs):
        super(UserRegistrationForm, self).__init__(*args, **kargs)

    class Meta:
        model = models.User
        fields = ('email', 'first_name', 'last_name', 'patronymic',)


class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('index')
