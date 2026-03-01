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


def get_bounds(years):
	bounds = {}
	for year in years:
		bounds[year] = (
			parser.parse(f"{year}-01-01 00:00:01+00:00"),
			parser.parse(f"{year}-12-31 23:59:59+00:00")
		)
	return bounds

def get_songs(years, write_out=False):
	"""
	Get the songs that were liked in a a list of years

	Args:
		year (list): list of all the years to get liked songs for.
		write_out (bool): optional flag to write the data out to as a csv

	Returns:
		list: Return list of each liked song in format ["artist", "song", "album", "same-year-release", "date-liked"]
	"""
	start_time = time.perf_counter()
	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
	# create date bounds
	bounds = get_bounds(years)

	# iterate songs and filter
	results = sp.current_user_saved_tracks()
	liked = {}
	for year in years:
		liked[year] = []
	header = ["artist", "song", "album", "same-year-release", "date-liked"]
	seen = 0
	print(f"Start processing liked songs for {', '.join(years)}...")
	while results:
		for item in results['items']:
			seen += 1
			added_at = parser.parse(item["added_at"])
			for year in years:
				if (added_at <= bounds[year][1] and added_at >= bounds[year][0]):
					track = item['track']
					release_date = track["album"]["release_date"]
					same_year = release_date[:4] == year
					liked[year].append([", ".join([artist["name"] for artist in track["artists"]]), track["name"], track["album"]["name"], same_year, item["added_at"]])
					# if this song was from this year it can't be from another one so skip any of the other years we're checking for
					break
		if results["next"]:
			results = sp.next(results)
		else:
			results = None
		output = f"Processed: {seen} songs"
		print(output, end='\r', flush=True)

	# sort tracks by artist
	print(f"Reviewed a total of {seen} songs")
	for year in years:
		print(f"Got {len(liked[year])} liked songs in {year}...")
		liked[year] = sorted(liked[year], key=lambda x: x[0][0].lower())

	# write out CSV
	if write_out is not None:
		for year in years:
			outfile = f"liked-songs-{year}.csv"
			print(f"Write out CSV {outfile}...")
			with open(outfile, 'w', newline='', encoding='utf-8') as outstream:
				writer = csv.writer(outstream)
				writer.writerow(header)
				for song in liked[year]:
					writer.writerow(song)
	else:
		print("No output file specified")
	elapsed_time = time.perf_counter() - start_time
	print(f"Finished in {math.floor(elapsed_time / 60)}:{(elapsed_time % 60):.1f}!")
	return liked

def main():
	load_dotenv()
	parser = argparse.ArgumentParser(
		prog='liked-by-year',
		description='Get the songs that were liked in Spotify in a calendar year.')
	parser.add_argument('years', help='Year(s) to get songs for e.g. 2019. For multiple years just keep adding as separate args', nargs='+')
	parser.add_argument('--output', '-o', action="store_true", help='Flag to output to CSV files')
	args = parser.parse_args()

	get_songs(args.years, args.output)


if __name__ == '__main__':
	main()
