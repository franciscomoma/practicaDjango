from django.contrib.auth.models import User
from django.contrib.auth.views import login, logout
from django.views.generic import CreateView
from django.forms.widgets import PasswordInput


def do_login(request):
    return login(request, redirect_field_name='/', template_name='login.html')

def do_logout(request):
    return logout(request, next_page='/')

class RegisterView(CreateView):
    model = User
    fields = ['username','first_name','last_name','email','password']

    def get_form(self, form_class=None):
        form = super(RegisterView, self).get_form(form_class)
        form.fields['password'].widget = PasswordInput()
        return form
