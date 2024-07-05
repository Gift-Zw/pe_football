from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_control
from core.admin import UserCreationForm
from core.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .models import SchoolProfile, TournamentRegistration, Player, TournamentPlayer


# Create your views here.

class UserRegistrationView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'schools/register_user.html'
    success_url = reverse_lazy('add-beneficiary')

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = User.objects.get(email=email)
        login(self.request, user)
        return redirect('add-beneficiary')


class UserLoginView(LoginView):
    template_name = 'schools/user_login.html'

    def get_success_url(self):
        if SchoolProfile.objects.filter(user=self.request.user).exists():
            return reverse_lazy('manager-dashboard')
        else:
            return reverse_lazy('add-beneficiary')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_logout_view(request):
    logout(request)
    return redirect('dashboard')


def dashboard_view(request):
    context = {}
    return render(request, 'schools/index.html', context)


def upcoming_tournaments_view(request):
    context = {}
    return render(request, 'schools/upcoming_tournaments.html', context)


def registered_tournaments_view(request):
    context = {}
    return render(request, 'schools/registered_tournaments.html', context)


def results_list_view(request):
    context = {}
    return render(request, 'schools/result_list.html', context)


def players_list_view(request):
    context = {}
    return render(request, 'schools/player_list.html', context)


def create_player_view(request):
    context = {}
    return render(request, 'schools/create_player.html', context)


def create_school_profile_view(request):
    context = {}
    return render(request, 'schools/create_school_profile.html', context)
