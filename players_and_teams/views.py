from django.shortcuts import render, redirect, HttpResponse
import requests
from .models import Player, Team
from .forms import PlayerForm, TeamForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def get_player(player_id):
    return Player.objects.get(id=player_id)

def get_team(team_id):
    return Team.objects.get(id=team_id)

@login_required
def player_list(request):
    players = Player.objects.filter(user=request.user)
    teams = Team.objects.filter(user=request.user)
    return render(request, 'players/player_team_list.html', {'players': players, 'teams': teams})

def player_detail(request, player_id):
    player = get_player(player_id)
    name_for_search = generate_search_name(player.last_name)
    r = requests.get(name_for_search)
    response = r.json()
    content = {
        'team_full': response['search_player_all']['queryResults']['row']['team_full'],
        'position': response['search_player_all']['queryResults']['row']['position'],
        'bats': response['search_player_all']['queryResults']['row']['bats'],
        'throws': response['search_player_all']['queryResults']['row']['throws'],
        'birth_country': response['search_player_all']['queryResults']['row']['birth_country'],
        'birth_date': response['search_player_all']['queryResults']['row']['birth_date'],
        'height_feet': response['search_player_all']['queryResults']['row']['height_feet'],
        'height_inches': response['search_player_all']['queryResults']['row']['height_inches'],
        'player': player
    }
    return render(request, 'players/player_detail.html', content)

def new_player(request):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.user = request.user
            player.save()
            return (player_list(request))
    else:
        form = PlayerForm()
    return render(request, 'players/player_form.html', {'form': form, 'type_of_request': 'New'}) 

def edit_player(request, player_id):
    player = get_player(player_id)
    if request.method == "POST":
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            player = form.save(commit=False)
            player.user = request.user
            player.save()
            return player_list(request)
    else:
        form = PlayerForm(instance=player)
    return render(request, 'players/player_form.html', {'form': form, 'type_of_request': 'Edit'})

def delete_player(request, player_id):
    if request.method == "POST":
        player = get_player(player_id)
        player.delete()
    return player_list(request)

def new_team(request):
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.user = request.user
            team.save()
            return (player_list(request))
    else:
        form = TeamForm()
    return render(request, 'teams/team_form.html', {'form': form, 'type_of_request': 'New'})

def edit_team(request, team_id):
    team = get_team(team_id)
    if request.method == "POST":
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            team = form.save(commit=False)
            team.user = request.user
            team.save()
            return player_list(request)
    else:
        form = TeamForm(instance=team)
    return render(request, 'teams/team_form.html', {'form': form, 'type_of_request': 'Edit'})

def delete_team(request, team_id):
    if request.method == "POST":
        team = get_team(team_id)
        team.delete()
    return player_list(request)

def generate_search_name(last_name):
    return f"http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code='mlb'&active_sw='Y'&name_part='{ last_name }%25'"

def news_creater(news):
    modified_news = news.replace(' ', '%20')
    news_api = "72c55bbd64484a56a24f37a30f2ea656"
    return f"https://newsapi.org/v2/everything?q={modified_news}&from=2021-03-26&sortBy=popularity&language=en&apiKey={news_api}"

@login_required
def news_detail(request):
    if request.method == "GET":
        query = request.GET.get('q')
        if query:
            response = requests.get(news_creater(query))
            try:
                if response.json()['status'] == 'ok':
                    json_data=response.json()['articles'][0:10]
                    article_list = []
                    for article in json_data:
                        current_article = {'title': article['title'], 'description':article ['description'], 'url': article['url']}
                        article_list.append(current_article)
                    return render(request, 'players/news_detail.html', {'term': query,    'articles':article_list})
                    
            except Exception as e:
                print(e)
                return HttpResponse(f"No results were found for {query}")










