# secret-library
![secret-library](./secret_library/library/static/assets/logo.svg)

secret-library is a self-hosted interactive fiction library and save file manager built on Django. Games can be scraped individually from the [Interactive Fiction Database (IFDB)](https://ifdb.org) and played in the browser with a modified version of [Parchment](https://github.com/curiousdannii/parchment) which supports saving over a web API. Save files are managed separately for each user.

Contributions are welcome!

## Usage Guide
When installed, log in to the "/admin/" page with the credentials admin/admin. It is recommended that you change the password for admin. Then, additional users can be created. Currently, all users can see and play the entire game library.

Games are scraped by entering the game's [TUID](https://ifdb.org/help-tuid) in the field on the "/library/scraper" page. There are four possible results after doing this.
- "Success": The game was found on IFDB and its data was downloaded into the database. **This does not necessarily mean it will play correctly**, as explained below.
- "Game with TUID {tuid} already present": The game was previously downloaded.
- "IFDB entry for {tuid} is invalid": The [IFDB API](https://ifdb.org/api/viewgame) result for the game did not contain information secret-library was expecting. This is most often an [IFID](https://ifdb.org/help-ifid). See [./secret_library/library/models.py](./secret_library/library/models.py) for the list of information secret-library's scraper expects.
- "No game {tuid} found on IFDB": IFDB could not find a game with that TUID in its database. This error will also be returned if IFDB is unreachable.

## Important Notes
This project is still in its early stages, and while the central functionality of save file management works, many features are rough or unfinished. If you find a bug or have a feature suggestion, please submit it as an issue.
- This webserver is not yet guaranteed to be secure. It is not yet recommended to expose it to the public Internet.
- Scraping from IFDB only works correctly if the game file is the topmost entry in the "External Links" section of the game's IFDB page. To work around this, scrape the game to get its metadata and then manually upload the correct game file through the "/admin/" page.

## Docker Compose Template
    services:
      secret-library:
        image: tordlemaster/secret-library:latest
        container_name: secret-library
        environment:
          # (Mapped to Django's SECRET_KEY setting) Generate your own Django secret key
          SECRET_KEY: "your_django_secret_key_here"

          # (Mapped to Django's ALLOWED_HOSTS setting) List all the IP addresses/root URLs that you wish secret-library to be available at as a comma-separated list. Do not wrap values in quotes.
          ALLOWED_HOSTS: ""
        ports:
          # Change the first number to the host port you wish secret-library to be available on
          - '8000:8000'
        restart: unless-stopped
        volumes:
          # Change the left of the following two lines to the appropriate directories in your host filesystem
          - /path/to/media/folder:/app/secret-library/sl_media
          - /path/to/database/folder:/app/secret-library/db
[Docker Hub page](https://hub.docker.com/r/tordlemaster/secret-library)

## Build Instructions
To build the modified version of Parchment developed for secret-library, replace the "asyncglk" submodule of Parchment with [asyncglk-sl](https://github.com/Tordlemaster/asyncglk-sl). Then build Parchment as instructed. To copy the appropriate files over, run the included transfer.sh script from the root directory of Parchment. Make sure to set the value of the SECRET_LIBRARY_ROOT environment variable to the absolute filepath of the root directory of secret-library (ending with a slash) first.