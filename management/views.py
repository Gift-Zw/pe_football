from django.shortcuts import render


# Create your views here.


def dashboard_view(request):
    context = {}
    return render(request, 'management/manager_dash.html', context)


def player_list_view(request):
    context = {}
    return render(request, 'management/player_list.html', context)


def player_profile_view(request):
    context = {}
    return render(request, 'management/player_profile.html', context)


def upcoming_tournament_list_view(request):
    context = {}
    return render(request, 'management/upcoming_tournament_list.html', context)


def past_tournament_list_view(request):
    context = {}
    return render(request, 'management/past_tournament_detail_view.html', context)


def tournament_detail_view(request):
    context = {}
    return render(request, 'management/tournament_list.html', context)


def results_list_view(request):
    context = {}
    return render(request, 'management/result_list.html', context)
