from django import forms
from .models import SchoolProfile, Player, TournamentRegistration, TournamentPlayer
from core.models import User
from management.models import Tournament

PLAYER_POSITIONS = (
    ('Goalkeeper', 'Goalkeeper'),
    ('Defender', 'Defender'),
    ('Midfielder', 'Midfielder'),
    ('Forward', 'Forward'),
)


class SchoolProfileForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    city = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    province = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    logo = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )


class PlayerForm(forms.Form):
    passport_photo = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    national_id = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    national_id_image = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    birth_certificate = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    grade_7_result = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    middle_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    birth_certificate_number = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    guardian_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    guardian_relationship = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    guardian_contact = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    present_school = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    year_enrolled = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    previous_school = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    cell = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    position = forms.ChoiceField(
        choices=PLAYER_POSITIONS,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class TournamentRegistrationForm(forms.Form):
    proof_of_payment = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )


class TournamentPlayerForm(forms.Form):
    tournament = forms.ModelChoiceField(
        queryset=Tournament.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    player = forms.ModelChoiceField(
        queryset=Player.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
