from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='admin_login'),
    path('dashboard/', views.dashboard_view, name='admin_dashboard'),
    path('past-tournaments-list/', views.past_tournament_list_view, name='admin_past_tournaments-list'),
    path('upcoming-tournaments-list/', views.upcoming_tournament_list_view, name='admin_upcoming_tournaments-list'),
    path('tournament-detail/<int:id>/', views.tournament_detail_view, name="admin_tournament_detail"),
    path('tournament-registrations/', views.tournament_registrations_view, name="admin_tournament_registration"),
    path('tournament-approval/<int:id>/', views.registration_approval_view, name="admin_tournament_approval"),
    path('tournament-players/', views.tournament_players_view, name="admin_tournament_players"),
    path('generate-id/<int:player_id>/', views.generate_id_card, name='generate_id_card'),
    path('results-list/', views.results_list_view, name="admin_result_list"),
    path('schools/', views.schools_view, name="admin_schools"),
    path('gallery-posts/', views.gallery_posts_view, name="admin_gallery"),
    path('players/', views.player_list_view, name="admin_player_list"),
    path('player-profile/<int:id>/', views.player_profile_view, name="admin_player_profile"),
    path('logout/', views.logout_view, name="admin_logout"),
    path('users/', views.users_view, name="admin_users"),
    # path('tournaments/<int:tournament_id>/approve/', views.approve_tournament_registration, name='approve_tournament_registration'),
    # path('tournaments/<int:tournament_id>/players/', views.view_tournament_players, name='view_tournament_players'),
    # path('tournaments/<int:tournament_id>/results/', views.upload_tournament_results, name='upload_tournament_results'),
]
