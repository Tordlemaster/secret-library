from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse

import save_api.pybase32k as pybase32k

from pathlib import Path
import os
import shutil

import json

# Create your views here.
def api(request):
    if request.method == "POST":
        body = json.loads(request.body)
        action = body.get('action')
        print(f"Save API Request: {action}, {body}")
        match action:
            case "get_all_user_data":
                #return HttpResponse("{}")
                pybase32k.build_lookup()
                filesystem_dict = dict()
                dialog_metadata = dict()
                for dirpaths, dirnames, filenames in os.walk(Path("./././save_files/")):
                    #print("new iteration")
                    for f in filenames:
                        filepath = os.path.join(dirpaths, f)
                        trimmed_filepath = filepath[filepath.find('\\'):].replace("\\", "/")
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
                        os.utime(Path("./././save_files" + file_path), (int(times.get('atime'))/1000, int(times.get('mtime'))/1000))
                else:
                    pybase32k.build_lookup()
                    file_content = pybase32k.decode(body.get('value'))
                    file_path = Path("./././save_files" + body.get('key'))
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    file_path.write_bytes(file_content)
                return HttpResponse("{}")
            
            case "remove":
                fp = body.get('key');
                try:
                    os.remove(Path("./././save_files" + fp))
                    if fp[-4:] == ".dir":
                        shutil.rmtree(Path("./././save_files" + fp[:-4]))
                except e:
                    pass
                return HttpResponse("{}")
            
        raise Http404("Save API unimplemented")
    else:
        raise Http404("Wrong HTTP Message Type")