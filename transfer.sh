#!bin/bash

if [[ -z "${SECRET_LIBRARY_ROOT}" ]]; then
  echo "You must set the value of the SECRET_LIBRARY_ROOT environment variable.
else
  rm -rf "$SECRET_LIBRARY_ROOT"secret_library/webplay/static/fonts
  rm -rf "$SECRET_LIBRARY_ROOT"secret_library/webplay/static/tools
  rm -rf "$SECRET_LIBRARY_ROOT"secret_library/webplay/static/web

  cp -a ./dist/. "$SECRET_LIBRARY_ROOT"secret_library/webplay/static/
  cp -a ./src/common/ui/LoadingPane.svelte "$SECRET_LIBRARY_ROOT"secret_library/webplay/static/web
  cp -a ./src/upstream/asyncglk/src/dialog/browser/ui/. "$SECRET_LIBRARY_ROOT"secret_library/webplay/static/web
fi