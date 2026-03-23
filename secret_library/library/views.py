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
import html
from django.utils.html import strip_tags
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def overview(request):
    game_list = Game.objects.order_by("-datetime_added")
    return render(request, "overview.html", {"username": request.user.username, "game_list": game_list})

@login_required
def gameview(request, tuid):
    try:
        game = Game.objects.get(tuid=tuid)
        return render(request, 'gameview.html', {"username": request.user.username, "game": game})
    except:
        raise Http404(f"No game with TUID {tuid} could be found.")

@login_required
def scraper(request):
    if request.method == "GET":
        return render(request, "scraper.html", {"username": request.user.username})
    
    elif request.method == "POST":
        tuid = request.POST["tuid"]
        
        ifdb_query = requests.get("https://ifdb.org/viewgame?json&id=" + tuid)
        print(ifdb_query)
        if ifdb_query.ok:
            q = ifdb_query.json()
            try:
                Game.objects.get(tuid = tuid)
                messages.success(request, f"Game with TUID {tuid} already present")
                return redirect("scraper")
            except:
                try:
                    game_file_content = requests.get(q['ifdb']['downloads']['links'][0]['url'], stream=True)
                    coverart_file_content = requests.get(q['ifdb']['coverart']['url'], stream=True)
                    game_file_content.raise_for_status()
                    coverart_file_content.raise_for_status()

                    game_folder: Path = Path(f"gamedata/{tuid}")
                    game_file_path: Path = game_folder / q['ifdb']['downloads']['links'][0]['url'].rpartition("/")[2]
                    coverart_file_path: Path = game_folder / ((q['ifdb']['downloads']['links'][0]['url'].rpartition("/")[2]).split(".")[0] + ".png")

                    tuid = tuid
                    ifid = q['identification']['ifids'][0]
                    title = q['bibliographic']['title']
                    author = q['bibliographic']['author']
                    publication_year = q['bibliographic']['firstpublished'][0:4]
                    description = strip_tags(html.unescape(q['bibliographic']['description']))
                    datetime_added = datetime.now(timezone.utc)
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
                        ifid = ifid,
                        title = title,
                        author = author,
                        publication_year = publication_year,
                        description = description,
                        datetime_added = datetime_added
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
                    messages.success(request, "Success")
                    return redirect("scraper")
                except Exception as e:
                    print(e)
                    messages.error(request, f"IFDB entry for {tuid} is invalid")
                    return redirect("scraper")
        else:
            #dirty hack
            messages.error(request, f"No game {tuid} found on IFDB")
            return redirect("scraper")
    else:
        Http404()