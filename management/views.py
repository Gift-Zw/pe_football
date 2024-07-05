from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from .models import Tournament, TournamentResults
from schools.models import SchoolProfile, Player, TournamentPlayer, TournamentRegistration
from .forms import TournamentForm, TournamentResultsForm
from django import forms


STAGE_CHOICES = [
    ('Group Stage', 'Group Stage'),
    ('Quarter Final', 'Quarter Final'),
    ('Semi Final', 'Semi Final'),
    ('Round of 16', 'Round of 16'),
    ('Final', 'Final'),
]


def dashboard_view(request):
    context = {}
    return render(request, 'management/manager_dash.html', context)


def player_list_view(request):
    context = {
        'players': Player.objects.all()
    }
    return render(request, 'management/player_list.html', context)


def player_profile_view(request):
    context = {}
    return render(request, 'management/player_profile.html', context)


def upcoming_tournament_list_view(request):
    if request.method == "POST":
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = Tournament.objects.create(
                name=form.data['name'],
                start_date=form.data['start_date'],
                venue=form.data['venue'],
                description=form.data['description'],
                time=form.data['time'],
                participation_fee=form.data['participation_fee'],
                age_limit=form.data['age_limit']
            )
            tournament.save()
            return redirect('management:admin_upcoming_tournaments-list')
        else:
            messages.error(request, form.errors)

    else:
        form = TournamentForm()

    context = {
        'tournaments': Tournament.objects.all(),
        'form': TournamentForm()
    }
    return render(request, 'management/upcoming_tournament_list.html', context)


def past_tournament_list_view(request):
    context = {
        'tournaments': Tournament.objects.all()
    }
    return render(request, 'management/past_tournament_list_view.html', context)


def tournament_detail_view(request, id):
    tournament = Tournament.objects.filter(id=id).first()

    class InTournamentResultsForm(forms.Form):
        school1 = forms.ModelChoiceField(
            queryset=SchoolProfile.objects.all(),
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        school2 = forms.ModelChoiceField(
            queryset=SchoolProfile.objects.all(),
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        school1_score = forms.IntegerField(
            widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        school2_score = forms.IntegerField(
            widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        stage = forms.ChoiceField(
            choices=STAGE_CHOICES,
            widget=forms.Select(attrs={'class': 'form-control'})
        )

    if request.method == "POST":
        form = InTournamentResultsForm(request.POST)
        if form.is_valid():
            result = TournamentResults.objects.create(
                tournament=tournament,
                school1=form.data['school1'],
                school2=form.data['school2'],
                school1_score=form.data['school1_score'],
                school2_score=form.data['school2_score'],
                stage=form.data['stage']
            )
            result.save()
            return redirect('management:admin_tournament_detail', tournament.id)
        else:
            messages.error(request, form.errors)
    else:
        form = InTournamentResultsForm()

    context = {
        'tournament': tournament,
        'form': InTournamentResultsForm()
    }
    return render(request, 'management/tournament_details.html', context)


def tournament_players_view(request):
    context = {}
    return render(request, 'management/tournament_players.html', context)


def tournament_registrations_view(request):
    context = {}
    return render(request, 'management/tournament_registrations.html', context)


def schools_view(request):
    context = {
        'schools': SchoolProfile.objects.all()
    }
    return render(request, 'management/schools.html', context)


def users_view(request):
    context = {}
    return render(request, 'management/users.html', context)


def results_list_view(request):
    if request.method == "POST":
        form = TournamentResultsForm(request.POST)
        if form.is_valid():
            result = TournamentResults.objects.create(
                tournament=form.data['tournament'],
                school1=form.data['school1'],
                school2=form.data['school2'],
                school1_score=form.data['school1_score'],
                school2_score=form.data['school2_score'],
                stage=form.data['stage']
            )
            result.save()
            return redirect('management:admin_result_list')
        else:
            messages.error(request, form.errors)
    else:
        form = TournamentResultsForm()
    context = {
        'tournament_results': TournamentResults.objects.all(),
        'form': TournamentResultsForm()
    }
    return render(request, 'management/result_list.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    logout(request)
    return redirect('management:admin_dashboard')
