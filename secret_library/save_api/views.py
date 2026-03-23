from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

import save_api.pybase32k as pybase32k

from pathlib import Path
import os
import shutil

import json

# Create your views here.

@login_required
def api(request):
    if request.method == "POST":
        body = json.loads(request.body)
        action = body.get('action')
        print(f"Save API Request: {action}, {body}")
        usr_base_dir = settings.SAVE_FILE_PATH / str(request.user.pk)
        print(usr_base_dir)
        match action:
            case "get_all_user_data":
                #return HttpResponse("{}")
                pybase32k.build_lookup()
                filesystem_dict = dict()
                dialog_metadata = dict()
                for dirpaths, dirnames, filenames in os.walk(usr_base_dir):
                    #print("new iteration")
                    for f in filenames:
                        filepath = os.path.join(dirpaths, f)
                        trimmed_filepath = "/usr" + filepath.removeprefix(str(usr_base_dir)).replace("\\", "/")
                        print(filepath, trimmed_filepath)
                        dialog_metadata[trimmed_filepath] = {
                            "atime": int(os.path.getatime(filepath)*1000.0),
                            "mtime": int(os.path.getmtime(filepath)*1000.0)
                        }
                        file_contents = Path(filepath).read_bytes()
                        filesystem_dict[trimmed_filepath] = pybase32k.encode(file_contents)
                filesystem_dict["dialog_metadata"] = str(dialog_metadata).replace("\'", "`").replace("\"", "\'").replace("`", "\"")
                print(str(filesystem_dict).replace("\'", "`").replace("\"", "\'").replace("`", "\""))
                return JsonResponse(filesystem_dict)
            
            case "set":
                if body.get('key') == 'dialog_metadata':
                    #print(type(body.get('value')))
                    data = json.loads(body.get('value'))
                    #print(type(data), data)
                    for file_path in data.keys():
                        times = data[file_path]
                        #print(int(times.get('atime'))/1000, int(times.get('mtime'))/1000)
                        print((int(int(times.get('atime'))/1000), int(int(times.get('mtime'))/1000)))
                        os.utime((usr_base_dir / file_path.removeprefix('/usr/')).resolve(), (int(int(times.get('atime'))/1000), int(int(times.get('mtime'))/1000)))
                else:
                    pybase32k.build_lookup()
                    file_content = pybase32k.decode(body.get('value'))
                    file_path = usr_base_dir / body.get('key').removeprefix('/usr/')
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    file_path.write_bytes(file_content)
                return HttpResponse("{}")
            
            case "remove":
                fp = body.get('key');
                try:
                    os.remove(usr_base_dir / fp.removeprefix('/usr/'))
                    if fp[-4:] == ".dir":
                        shutil.rmtree(usr_base_dir / fp[:-4].removeprefix('/usr/'))
                except Exception as e:
                    print(e)
                return HttpResponse("{}")
            
        raise Http404("Save API unimplemented")
    else:
        raise Http404("Wrong HTTP Message Type")