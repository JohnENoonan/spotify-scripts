# Spotify Scripts
A series of python scripts that extract personal archival data

## Inspiration
These scripts were designed primarily for archiving personal liked songs and for looking into deeper trends in my own listening

## Installation

### Python
* Install python > 3.10
* In a terminal go into this repo and run `pip install -r requirements.txt`

### Spotify
* Follow the [Spotipy app setup instructions](https://github.com/spotipy-dev/spotipy/blob/2.22.1/TUTORIAL.md#step-1-creating-a-spotify-account)
* In this repo create a `.env` file with the following fields filled in
	```bash
	SPOTIPY_CLIENT_ID=...
	SPOTIPY_CLIENT_SECRET=...
	SPOTIPY_REDIRECT_URI=http://localhost:1234/
	```

## Running 
Each script uses Argparser, simply run the python scripts from the CLI with the appropriate arguments. The `--help` argument will ist all possible arguments. 

## License
This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
