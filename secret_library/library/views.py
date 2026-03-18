from django.shortcuts import render
from django.http import HttpResponse, Http404

import requests
from pathlib import Path
from .models import Game
from django.conf import settings
from django.core.files import File

# Create your views here.
def overview(request):
    return HttpResponse("Games Overview")

def scraper(request):
    if request.method == "GET":
        return render(request, "scraper.html")
    if request.method == "POST":
        tuid = request.POST["tuid"]
        
        ifdb_query = requests.get("https://ifdb.org/viewgame?json&id=" + tuid)
        print(ifdb_query)
        if ifdb_query.ok:
            q = ifdb_query.json()
            try:
                Game.objects.get(tuid = tuid)
            except:
                game_file_content = requests.get(q['ifdb']['downloads']['links'][0]['url'], stream=True)
                coverart_file_content = requests.get(q['ifdb']['coverart']['url'], stream=True)
                game_file_content.raise_for_status()
                coverart_file_content.raise_for_status()

                game_folder: Path = settings.MEDIA_ROOT / f"gamedata/{tuid}"
                game_file_path: Path = game_folder / q['ifdb']['downloads']['links'][0]['url'].rpartition("/")[2]
                coverart_file_path: Path = game_folder / ((q['ifdb']['downloads']['links'][0]['url'].rpartition("/")[2]).split(".")[0] + ".png")

                game_folder.mkdir(parents=True, exist_ok=True)
                game_file_path.write_bytes(game_file_content.content)
                coverart_file_path.write_bytes(coverart_file_content.content)
                
                new_game = Game(
                    tuid = tuid,
                    ifid = q['identification']['ifids'][0],
                    title = q['bibliographic']['title'],
                    author = q['bibliographic']['author'],
                    publication_year = q['bibliographic']['firstpublished'],
                    description = q['bibliographic']['description'],
                )

                with game_file_path.open(mode="rb") as g, coverart_file_path.open(mode="rb") as c:
                    new_game.game_file = File(g, name=game_file_path.name)
                    new_game.coverart_file = File(c, name=coverart_file_path.name)
                    new_game.save()
        return HttpResponse(str(tuid))
    else:
        Http404()