# Shows a user's saved tracks (need to be authenticated via oauth)

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import argparse
import csv
from dateutil import parser
import os
import math
from dotenv import load_dotenv
import time



load_dotenv()
scope = 'user-library-read'

def get_songs(year, outfile):
    start_time = time.perf_counter()
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    # create date bounds
    min_date = parser.parse(f"{year}-01-01 00:00:01+00:00")
    max_date = parser.parse(f"{year}-12-31 23:59:59+00:00")

    # iterate songs and filter
    results = sp.current_user_saved_tracks()
    liked = []
    header = ["artist", "song", "album", "same-year-release", "date-liked"]
    seen = 0
    print("Start processing liked songs...")
    while results:
        for idx, item in enumerate(results['items']):
            seen += 1
            added_at = parser.parse(item["added_at"])
            if (added_at <= max_date and added_at >= min_date):
                track = item['track']
                release_date = track["album"]["release_date"]
                same_year = release_date[:4] == year
                liked.append([", ".join([artist["name"] for artist in track["artists"]]), track["name"], track["album"]["name"], same_year, item["added_at"]])
        if (results["next"]):
            results = sp.next(results)
        else:
            results = None
        output = f"Processed: {seen} songs"
        print(output, end='\r', flush=True)

    # sort tracks by artist
    print(f"Got {len(liked)} out of {seen} songs. Sort by artist...")
    liked = sorted(liked, key=lambda x: x[0][0].lower())

    # write out CSV
    
    print("Write out CSV...")
    with open(outfile, 'w', newline='', encoding='utf-8') as outstream:
        writer = csv.writer(outstream)
        writer.writerow(header)
        for song in liked:
            writer.writerow(song)
    elapsed_time = time.perf_counter() - start_time
    print(f"Finished in {math.floor(elapsed_time / 60)}:{(elapsed_time % 60):.1f}!")

def main():
    parser = argparse.ArgumentParser(
        prog='liked-by-year',
        description='Get the songs that were liked in Spotify in a calendar year.')
    parser.add_argument('year', help='Year to get songs for e.g. 2019')
    parser.add_argument('--outfile', help='CSV file to write data out to')
    args = parser.parse_args()

    outfile = args.outfile
    if not outfile:
        outfile = f"liked-songs-{args.year}.csv"
    get_songs(args.year, outfile)


if __name__ == '__main__':
    main()