from django.urls import path
from . import views

app_name = 'players_and_teams'

urlpatterns = [
    path('', views.player_list, name='player_list'),
    path('new_player', views.new_player, name='new_player'),
    path('<int:player_id>', views.player_detail, name='player_detail'),
    path('<int:player_id>/edit', views.edit_player, name='edit_player'),
    path('<int:player_id>/delete', views.delete_player, name='delete_player'),
    path('new_team', views.new_team, name='new_team'),
    path('edit_team/<int:team_id>/edit', views.edit_team, name='edit_team'),
    path('delete_team/<int:team_id>/delete', views.delete_team, name='delete_team'),
    path('news', views.news_detail, name='news_detail'),
]