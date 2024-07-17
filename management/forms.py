from django import forms
from .models import Tournament, TournamentResults
from schools.models import SchoolProfile

STAGE_CHOICES = [
    ('Group Stage', 'Group Stage'),
    ('Quarter Final', 'Quarter Final'),
    ('Semi Final', 'Semi Final'),
    ('Round of 16', 'Round of 16'),
    ('Final', 'Final'),
]


class TournamentForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    venue = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    age_limit = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
    )
    participation_fee = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(

        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )


class TournamentResultsForm(forms.Form):
    tournament = forms.ModelChoiceField(
        queryset=Tournament.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
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


class MediaContentForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    youtube_url = forms.URLField(
        max_length=255,
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    cover_image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
