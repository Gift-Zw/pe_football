from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_control
from .models import Tournament, TournamentResults, MediaContent
from schools.models import SchoolProfile, Player, TournamentPlayer, TournamentRegistration
from .forms import TournamentForm, TournamentResultsForm, MediaContentForm
from django import forms
from .decorators import admin_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from PIL import Image, ImageDraw, ImageFont
import qrcode
from reportlab.pdfgen import canvas
from io import BytesIO
from pe_football import settings
import tempfile
import os


def generate_id_card(request, player_id):
    player = get_object_or_404(Player, id=player_id)

    # Load the ID card template
    template_path = settings.BASE_DIR / settings.STATIC_CYBER / 'id.jpeg'
    template = Image.open(template_path)

    # Create a drawing context
    draw = ImageDraw.Draw(template)

    # Define a larger font size
    heading_path = settings.BASE_DIR / settings.STATIC_CYBER / 'BRLNSDB.TTF'
    font_path = settings.BASE_DIR / settings.STATIC_CYBER / 'Humanist521LightBT.ttf'
    font = ImageFont.truetype(heading_path, 32)
    name_font = ImageFont.truetype(heading_path, 44)
    heading_font = ImageFont.truetype(font_path, 40)

    # Player detailss
    player_details = {
        'photo_path': player.passport_photo.path,  # Adjust as needed
        'dob': player.date_of_birth.strftime('%Y-%m-%d'),
        'national_id': player.national_id,
        'school': player.school.name,
        'name': player.first_name + ' ' + player.last_name,
        'position': player.position
    }

    # Positions on the ID card for each detail
    positions = {
        'name': (270, 282),
        'position': (270, 285),
        'photo': (270, 380),  # x, y coordinates for the photo
        'dob': (310, 697),
        'national_id': (310, 745),
        'school': (310, 800)
    }

    # Load and place the player's photo
    player_photo = Image.open(player_details['photo_path']).resize((250, 250))
    template.paste(player_photo, positions['photo'])

    # Draw text details with larger font size
    draw.text(positions['name'], f"{player_details['name']}", font=name_font, fill="white")
    draw.text(positions['dob'], f"{player_details['dob']}", font=font, fill="white")
    draw.text(positions['national_id'], f"{player_details['national_id']}", font=font, fill="white")
    draw.text(positions['school'], f"{player_details['school']}", font=font, fill="white")

    # Generate a QR code with player details
    qr_data = f"Name: {player.first_name} {player.last_name}\nDOB: {player_details['dob']}\nNational ID: {player_details['national_id']}"
    qr = qrcode.QRCode(box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill='black', back_color='white').convert('RGB')

    # Position and place the QR code on the ID card
    qr_position = (570, 900)  # x, y coordinates for the QR code
    qr_img = qr_img.resize((170, 170))  # Resize the QR code to fit on the card
    template.paste(qr_img, qr_position)

    # Save the ID card to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpeg')
    template.save(temp_file, 'JPEG')
    temp_file.close()

    # Read the temporary file and create an HTTP response with the image
    with open(temp_file.name, 'rb') as f:
        image_data = f.read()

    # Clean up the temporary file
    os.unlink(temp_file.name)

    response = HttpResponse(image_data, content_type='image/jpeg')
    response['Content-Disposition'] = f'inline; filename="{player.first_name}_{player.last_name}_id_card.jpeg"'

    return response


STAGE_CHOICES = [
    ('Group Stage', 'Group Stage'),
    ('Quarter Final', 'Quarter Final'),
    ('Semi Final', 'Semi Final'),
    ('Round of 16', 'Round of 16'),
    ('Final', 'Final'),
]


class UserLoginView(LoginView):
    template_name = 'management/user_login.html'

    def get_success_url(self):
        return reverse_lazy('management:admin_upcoming_tournaments-list')


@admin_required()
def dashboard_view(request):
    context = {}
    return render(request, 'management/manager_dash.html', context)


@admin_required()
def player_list_view(request):
    context = {
        'players': Player.objects.all(),
    }
    return render(request, 'management/player_list.html', context)


@admin_required()
def player_profile_view(request, id):
    player = Player.objects.filter(id=id).first()
    tournaments = TournamentPlayer.objects.filter(player=player).select_related('tournament')
    played_tournaments = [tp.tournament for tp in tournaments]
    context = {
        'player': player,
        'tournaments': tournaments
    }
    return render(request, 'management/player_profile.html', context)


@admin_required()
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


@admin_required()
def past_tournament_list_view(request):
    context = {
        'tournaments': Tournament.objects.all()
    }
    return render(request, 'management/past_tournament_list_view.html', context)


@admin_required()
def tournament_detail_view(request, id):
    tournament = Tournament.objects.filter(id=id).first()
    tournament_players = TournamentPlayer.objects.filter(tournament_id=id).select_related('player')
    players = [tp.player for tp in tournament_players]

    class InTournamentResultsForm(forms.Form):
        school1 = forms.ModelChoiceField(
            queryset=SchoolProfile.objects.filter(tournamentregistration__tournament=tournament),
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        school2 = forms.ModelChoiceField(
            queryset=SchoolProfile.objects.filter(tournamentregistration__tournament=tournament),
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
                school1=SchoolProfile.objects.get(id=form.data['school1']),
                school2=SchoolProfile.objects.get(id=form.data['school2']),
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
        'form': InTournamentResultsForm(),
        'registered_schools': SchoolProfile.objects.filter(tournamentregistration__tournament=tournament),
        'results': TournamentResults.objects.filter(tournament=tournament),
        'players': players
    }
    return render(request, 'management/tournament_details.html', context)


@admin_required()
def tournament_players_view(request):
    context = {}
    return render(request, 'management/tournament_players.html', context)


@admin_required()
def tournament_registrations_view(request):
    context = {
        'regs': TournamentRegistration.objects.all()
    }
    return render(request, 'management/tournament_registrations.html', context)


@admin_required()
def registration_approval_view(request, id):
    registration = get_object_or_404(TournamentRegistration, id=id)
    registration.approved = True
    registration.save()
    messages.success(request, 'Registration status has been updated.')
    return redirect('management:admin_tournament_registration')


@admin_required()
def schools_view(request):
    context = {
        'schools': SchoolProfile.objects.all()
    }
    return render(request, 'management/schools.html', context)


@admin_required()
def users_view(request):
    context = {}
    return render(request, 'management/users.html', context)


@admin_required()
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


@admin_required()
def gallery_posts_view(request):
    if request.method == "POST":
        form = MediaContentForm(request.POST, request.FILES)
        if form.is_valid():
            result = MediaContent.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                youtube_url=form.cleaned_data['youtube_url'],
                cover_image=form.cleaned_data['cover_image']
            )
            result.save()
            return redirect('management:admin_gallery')
        else:
            messages.error(request, form.errors)
    else:
        form = MediaContentForm()
    context = {
        'media_content': MediaContent.objects.all(),
        'form': MediaContentForm()
    }
    return render(request, 'management/gallery_posts.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    logout(request)
    return redirect('management:admin_dashboard')
