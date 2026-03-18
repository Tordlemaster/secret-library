from django.shortcuts import render
from django.http import Http404
from library.models import Game

from django.conf import settings

# Create your views here.
def index(request, game_tuid):
    try:
        game = Game.objects.get(tuid=game_tuid)
        return render(request, 'index.html', {"gamefile": game.game_file.name})
    except:
        return Http404(f"No game with TUID {game_tuid} could be found.")