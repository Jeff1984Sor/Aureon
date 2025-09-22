# contas/views.py
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm # Usa o form padrão

from .forms import CustomUserCreationForm

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'contas/signup.html'

class CustomLoginView(LoginView):
    template_name = 'contas/login.html'
    # Agora usa o formulário de autenticação padrão do Django, sem o campo 'empresa'
    authentication_form = AuthenticationForm