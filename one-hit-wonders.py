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


scope = 'user-library-read'

class Artist:
	def __init__(self, name):
		self.name = name
		self.songs = []

	def __eq__(self, other):
		if not isinstance(other, Artist):
			return NotImplemented
		return self.name == other.name

	def __lt__(self, other): 
		return self.name.lower() < other.name.lower()
	
	def __hash__(self):

		return hash(self.name)

	def __repr__(self):
		return f"'{self.name}': {len(self.songs)} songs"

def get_one_hit(outfile=None):
	"""
	Get the songs/artists from your likes that are unique

	Args:
		outfile (str): optional path to write the data out to as a vsv

	Returns:
		list: Return list of each liked song in format ["artist", "song", "album", "same-year-release", "date-liked"]
	"""
	start_time = time.perf_counter()
	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
	# create date bounds

	# iterate songs and filter
	results = sp.current_user_saved_tracks()
	header = ["artist", "song", "album", "release-date", "date-liked"]
	seen = 0
	all_artists = set()
	one_hit = set()
	print("Start processing liked songs...")
	while results:
		for item in results['items']:
			seen += 1
			track = item['track']			
			artists = Artist(", ".join([artist["name"] for artist in track["artists"]]))
			# new artist
			if artists not in all_artists:
				artists.songs.append([track["name"], track["album"]["name"], track["album"]["release_date"], item["added_at"]])
				all_artists.add(artists)
				one_hit.add(artists)
			# if this artist has been seen before and is currently a one hit we must remove them
			elif artists in one_hit:
				one_hit.remove(artists)

		if results["next"]:
			results = sp.next(results)
		else:
			results = None
		output = f"Processed: {seen} songs"
		print(output, end='\r', flush=True)
	# sort tracks by artist
	print(f"Got {len(one_hit)} one-hit-wonders out of {seen} total songs. Sort by artist...")
	one_hit = sorted(list(one_hit))
	# write out CSV
	if outfile is not None:
		print("Write out CSV...")
		with open(outfile, 'w', newline='', encoding='utf-8') as outstream:
			writer = csv.writer(outstream)
			writer.writerow(header)
			for artist in one_hit:
				if (len(artist.songs) > 1):
					print(artist)
				writer.writerow([artist.name] + artist.songs[0])
	else:
		print("No output file specified")
	elapsed_time = time.perf_counter() - start_time
	print(f"Finished in {math.floor(elapsed_time / 60)}:{(elapsed_time % 60):.1f}!")
	return one_hit

def main():
	load_dotenv()
	parser = argparse.ArgumentParser(
		prog='liked-one-hits',
		description='Get the songs/artists that are personal one-hit-wonders.')
	parser.add_argument('--outfile', help='CSV file to write data out to')
	args = parser.parse_args()

	outfile = args.outfile
	get_one_hit(outfile)


if __name__ == '__main__':
	main()