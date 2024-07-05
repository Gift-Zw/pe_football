from django.urls import path
from . import views

app_name = 'schools'

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='school_register'),
    path('login/', views.UserLoginView.as_view(), name='school_login'),
    path('dashboard/', views.dashboard_view, name='school_dashboard'),
    path('upcoming-tournaments/', views.upcoming_tournaments_view, name='upcoming_tournaments'),
    path('registerd-tournaments/', views.registered_tournaments_view, name='registered_tournaments'),
    path('player-list/', views.players_list_view, name='player_list'),
    path('players/create/', views.create_player_view, name='create_player'),
    path('result-list/', views.results_list_view, name='result_list'),
    # path('tournaments/<int:tournament_id>/players/', views.select_players, name='select_players'),
]
