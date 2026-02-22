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
Each script uses Argparser, simply run the pytjhon scripts from the CLI with the appropriate arguments
