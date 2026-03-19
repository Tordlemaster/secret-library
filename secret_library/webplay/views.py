from django.shortcuts import render
from django.http import Http404
from library.models import Game
from django.contrib.auth.decorators import login_required

from django.conf import settings

# Create your views here.

@login_required
def index(request, tuid):
    try:
        game = Game.objects.get(tuid=tuid)
        return render(request, 'index.html', {"gamefile": game.game_file.name})
    except:
        raise Http404(f"No game with TUID {tuid} could be found.")