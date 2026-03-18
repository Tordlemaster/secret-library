from django.shortcuts import render
from django.http import HttpResponse, Http404

import requests
from pathlib import Path
from .models import Game
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from datetime import datetime, timezone

# Create your views here.
def overview(request):
    game_list = Game.objects.order_by("-datetime_added")
    return render(request, "overview.html", {"game_list": game_list})

def gameview(request, tuid):
    try:
        game = Game.objects.get(tuid=tuid)
        return render(request, 'gameview.html', {"game": game})
    except:
        raise Http404(f"No game with TUID {tuid} could be found.")

def scraper(request, msg_class, msg_text):
    if request.method == "GET":
        return render(request, "scraper.html", {"msg_class": msg_class, "msg_text": msg_text})
    
    if request.method == "POST":
        tuid = request.POST["tuid"]
        
        ifdb_query = requests.get("https://ifdb.org/viewgame?json&id=" + tuid)
        print(ifdb_query)
        if ifdb_query.ok:
            q = ifdb_query.json()
            try:
                Game.objects.get(tuid = tuid)
                #dirty hack
                request.method = "GET"
                return scraper(request, "success", f"{tuid} already present")
            except:
                game_file_content = requests.get(q['ifdb']['downloads']['links'][0]['url'], stream=True)
                coverart_file_content = requests.get(q['ifdb']['coverart']['url'], stream=True)
                game_file_content.raise_for_status()
                coverart_file_content.raise_for_status()

                game_folder: Path = settings.MEDIA_ROOT / f"gamedata/{tuid}"
                game_file_path: Path = game_folder / q['ifdb']['downloads']['links'][0]['url'].rpartition("/")[2]
                coverart_file_path: Path = game_folder / ((q['ifdb']['downloads']['links'][0]['url'].rpartition("/")[2]).split(".")[0] + ".png")

                game_folder.mkdir(parents=True, exist_ok=True)

                #avoid duplication of files
                '''print(game_file_path, game_file_path.is_file())
                print(coverart_file_path, coverart_file_path.is_file())
                if not game_file_path.is_file():
                    print("Writing game file")
                    game_file_path.write_bytes(game_file_content.content)
                if not coverart_file_path.is_file():
                    print("Writing cover art file")
                    coverart_file_path.write_bytes(coverart_file_content.content)'''
                
                new_game = Game(
                    tuid = tuid,
                    ifid = q['identification']['ifids'][0],
                    title = q['bibliographic']['title'],
                    author = q['bibliographic']['author'],
                    publication_year = q['bibliographic']['firstpublished'],
                    description = q['bibliographic']['description'],
                    datetime_added = datetime.now(timezone.utc)
                )
                print(game_file_path.name, coverart_file_path.name)
                new_game.game_file.save(game_file_path, ContentFile(game_file_content.content), save=False)
                new_game.coverart_file.save(coverart_file_path, ContentFile(coverart_file_content.content), save=False)
                new_game.save()

                '''with game_file_path.open(mode="rb") as g, coverart_file_path.open(mode="rb") as c:
                    new_game.game_file = File(g, name=game_file_path.name)
                    new_game.coverart_file = File(c, name=coverart_file_path.name)
                    new_game.save()'''
                #dirty hack
                request.method = "GET"
                return scraper(request, "success", "Success")
        else:
            #dirty hack
            request.method = "GET"
            return scraper(request, "failure", f"No game {tuid} on IFDB")
    else:
        Http404()