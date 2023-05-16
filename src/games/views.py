from django.shortcuts import render, get_object_or_404
from .models import Game, GameData

# Pagination 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index(request):
    search = request.POST.get('search')
    games = Game.objects.all().order_by('name')
    if search:
        games = Game.objects.filter(name__contains=search).order_by('name')

    paginator = Paginator(games, 21)
    page = request.GET.get('page')
    game_list = paginator.get_page(page)
    items=[]
    for game in game_list:
        game_datas = GameData.objects.filter(game=game).order_by('-date')
        items.append({'game':game, 'datas': game_datas[0]} )

    return render(request, 'games/index.html', {'games': game_list, 'items': items, 'search': search})


# def game_search(request, text):
#     games = Game.objects.filter(name__icontains=text).order_by('name')
#     paginator = Paginator(games, 21)
#     page = request.GET.get('page')
#     game_list = paginator.get_page(page)
#     items=[]
#     for game in game_list:
#         game_datas = GameData.objects.filter(game=game).order_by('-date')
        
#         items.append({'game':game, 'datas': game_datas[0]} )

#     return render(request, 'games/index.html', {'games': game_list, 'items': items})


def game_detail(request, slug):
    game = get_object_or_404(Game, slug=slug)
    game_datas = GameData.objects.filter(game=game).order_by('-date')
    return render(request, 'games/game_detail.html', {'game': game, 'game_datas': game_datas})
