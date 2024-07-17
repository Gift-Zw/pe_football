from django.shortcuts import render
from management.models import Tournament, TournamentResults, MediaContent
from schools.models import SchoolProfile, Player
# Create your views here.


def home_view(request):
    ctx = {
        'tournament': Tournament.objects.last(),
        'result': TournamentResults.objects.last(),
        'total_games': TournamentResults.objects.all().count(),
        'total_players': Player.objects.all().count(),
        'total_tournaments': Tournament.objects.all().count(),
        'total_schools': SchoolProfile.objects.all().count()
    }
    return render(request, 'core/index.html', ctx)


def gallery_view(request):
    ctx = {
        'media_content': MediaContent.objects.all()
    }
    return render(request, 'core/gallery.html', ctx)



def result_view(request):
    ctx = {
        'results': TournamentResults.objects.all()
    }
    return render(request, 'core/results.html', ctx)



def tournament_view(request):
    ctx = {
        'tournaments': Tournament.objects.all()
    }
    return render(request, 'core/tournaments.html', ctx)