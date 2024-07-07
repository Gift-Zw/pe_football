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
from .forms import SchoolProfileForm, PlayerForm, TournamentPlayerForm, TournamentRegistrationForm
from management.models import Tournament, TournamentResults
from .decorators import school_required


# Create your views here.

class UserRegistrationView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'schools/register_user.html'
    success_url = reverse_lazy('schools:create_school_profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = User.objects.get(email=email)
        login(self.request, user)
        return redirect('schools:create_school_profile')


class UserLoginView(LoginView):
    template_name = 'schools/user_login.html'

    def get_success_url(self):
        if SchoolProfile.objects.filter(user=self.request.user).exists():
            return reverse_lazy('schools:school_dashboard')
        else:
            return reverse_lazy('schools:create_school_profile')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_logout_view(request):
    logout(request)
    return redirect('schools:school_login')


@school_required()
def dashboard_view(request):
    profile = SchoolProfile.objects.filter(user=request.user).first()
    name = profile.name
    logo = profile.logo
    context = {
        'name': name,
        'logo': logo.url
    }
    return render(request, 'schools/index.html', context)


@school_required()
def upcoming_tournaments_view(request):
    profile = SchoolProfile.objects.filter(user=request.user).first()
    name = profile.name
    logo = profile.logo
    context = {
        'tournaments': Tournament.objects.all(),
        'name': name,
        'logo': logo.url,
    }
    return render(request, 'schools/upcoming_tournaments.html', context)


@school_required()
def registered_tournaments_view(request):
    profile = SchoolProfile.objects.filter(user=request.user).first()
    name = profile.name
    logo = profile.logo
    context = {
        'name': name,
        'logo': logo.url,
    }
    return render(request, 'schools/registered_tournaments.html', context)


@school_required()
def results_list_view(request):
    profile = SchoolProfile.objects.filter(user=request.user).first()
    name = profile.name
    logo = profile.logo
    context = {
        'name': name,
        'logo': logo.url
    }
    return render(request, 'schools/result_list.html', context)


@school_required()
def players_list_view(request):
    profile = SchoolProfile.objects.filter(user=request.user).first()
    name = profile.name
    logo = profile.logo
    players = Player.objects.filter(school=profile)
    context = {
        'name': name,
        'logo': logo.url,
        'players': players
    }
    return render(request, 'schools/player_list.html', context)


@school_required()
def create_player_view(request):
    profile = SchoolProfile.objects.filter(user=request.user).first()
    name = profile.name
    logo = profile.logo
    if request.method == "POST":
        form = PlayerForm(request.POST, request.FILES)
        if form.is_valid():
            player = Player.objects.create(
                school=profile,
                passport_photo=form.cleaned_data['passport_photo'],
                national_id=form.cleaned_data['national_id'],
                national_id_image=form.cleaned_data['national_id_image'],
                birth_certificate=form.cleaned_data['birth_certificate'],
                grade_7_result=form.cleaned_data['grade_7_result'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                middle_name=form.cleaned_data['middle_name'],
                birth_certificate_number=form.cleaned_data['birth_certificate_number'],
                guardian_name=form.cleaned_data['guardian_name'],
                guardian_relationship=form.cleaned_data['guardian_relationship'],
                guardian_contact=form.cleaned_data['guardian_contact'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                present_school=form.cleaned_data['present_school'],
                year_enrolled=form.cleaned_data['year_enrolled'],
                previous_school=form.cleaned_data['previous_school'],
                cell=form.cleaned_data['cell'],
                position=form.cleaned_data['position']
            )

            player.save()
            return redirect('schools:player_list')
        else:
            messages.error(request, form.errors)

    context = {
        'form': PlayerForm(),
        'name': name,
        'logo': logo.url
    }
    return render(request, 'schools/create_player.html', context)


@school_required()
def player_profile_view(request, id):
    profile = SchoolProfile.objects.filter(user=request.user).first()
    name = profile.name
    logo = profile.logo
    player = Player.objects.filter(id=id).first()
    context = {
        'player': player,
        'name': name,
        'logo': logo.url
    }
    return render(request, 'schools/player_profile.html', context)


@school_required()
def register_tournament_view(request, id):
    tournament = Tournament.objects.filter(id=id)
    profile = SchoolProfile.objects.filter(user=request.user).first()
    name = profile.name
    logo = profile.logo
    context = {
        'tournament': tournament,
        'name': name,
        'logo': logo.url
    }
    return render(request, 'schools/tournament_view.html', context)


@school_required()
def tournament_detail_view(request, id):
    profile = SchoolProfile.objects.filter(user=request.user).first()
    name = profile.name
    logo = profile.logo
    tournament = Tournament.objects.filter(id=id).first()
    reg = TournamentRegistration.objects.filter(school=profile, tournament=tournament)

    if request.method == "POST":
        form = TournamentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            tournament_reg = TournamentRegistration.objects.create(
                school=profile,
                tournament=tournament,
                proof_of_payment=form.cleaned_data['proof_of_payment']
            )
            tournament_reg.save()
            return redirect('schools:tournament_detail', tournament.id)
        else:
            messages.error(request, form.errors)

    context = {
        'tournament': tournament,
        'name': name,
        'logo': logo.url,
        'form': TournamentRegistrationForm(),
        'is_registered': reg.exists(),
        'reg':reg.first()
    }
    return render(request, 'schools/tournament_view.html', context)


@school_required()
def create_school_profile_view(request):
    if request.method == "POST":
        form = SchoolProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = SchoolProfile.objects.create(
                user=request.user,
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                city=form.cleaned_data['city'],
                province=form.cleaned_data['province'],
                logo=form.cleaned_data['logo']
            )
            profile.save()
            return redirect('schools:school_dashboard')
        else:
            messages.error(request, form.errors)

    context = {
        'form': SchoolProfileForm()
    }
    return render(request, 'schools/create_school_profile.html', context)
