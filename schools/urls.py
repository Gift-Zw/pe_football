from django.urls import path
from . import views

app_name = 'schools'

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='school_register'),
    path('login/', views.UserLoginView.as_view(), name='school_login'),
    path('logout/', views.user_logout_view, name='school_logout'),
    path('dashboard/', views.dashboard_view, name='school_dashboard'),
    path('upcoming-tournaments/', views.upcoming_tournaments_view, name='upcoming_tournaments'),
    path('registerd-tournaments/', views.registered_tournaments_view, name='registered_tournaments'),
    path('register-tournament/<int:id>/', views.register_tournament_view, name='register_tournament'),
    path('tournament-detail/<int:id>/', views.tournament_detail_view, name='tournament_detail'),
    path('player-list/', views.players_list_view, name='player_list'),
    path('players/create/', views.create_player_view, name='create_player'),
    path('player-profile/<int:id>/', views.player_profile_view, name='player_profile'),
    path('result-list/', views.results_list_view, name='result_list'),
    path('create-school-profile/', views.create_school_profile_view, name='create_school_profile'),
    # path('tournaments/<int:tournament_id>/players/', views.select_players, name='select_players'),
]
