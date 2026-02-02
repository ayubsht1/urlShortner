from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .models import CustomUser
from .forms import UserRegisterForm

class RegisterView(CreateView):
    model = CustomUser
    form_class = UserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class EmailLoginView(LoginView):
    template_name = 'registration/login.html'