from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('results/', views.result_view, name='result'),
    path('tournaments/', views.tournament_view, name='tournaments'),
    # path('tournaments/', views.tournaments_list, name='tournaments_list'),
    # path('tournaments/<int:tournament_id>/', views.tournament_detail, name='tournament_detail'),
]
