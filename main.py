#! /usr/bin/env python

from collections import namedtuple
import re

import click
from funcy.seqs import first
import praw
import spotipy
import spotipy.util as util

scope = 'playlist-modify-public'
user_agent = 'subredditToPlaylist'

Track = namedtuple('Track', ['artist', 'track'])


def parse_title(s):
    val = re.split(' -+ ', s, 1)
    if len(val) == 2:
        artist = val[0].strip()
        track = re.split('\[', val[1], 1)[0].strip()
        return Track(artist, track)


def get_subreddit_tracks(subreddit, limit):
    """
    returns a parsed list of tracks from the given subreddit
    :param subreddit: subreddit name
    :param limit: number of posts to fetch
    :return: list of Track objects
    """
    r = praw.Reddit(user_agent=user_agent)
    submissions = list(r.get_subreddit(subreddit).get_top_from_month(limit=limit))
    return [parse_title(x.title) for x in submissions if parse_title(x.title)]


def generate_spotify_playlist(tracks, playlist_name, username):
    """
    Generates a Spotify playlist from the given tracks
    :param tracks: list of Track objects
    :param playlist_name: name of playlist to create
    :param username: Spotify username
    """
    sp = spotipy.Spotify()
    formatted_tracks = [u'artist:"{artist}" track:"{track}"'.format(artist=t.artist, track=t.track) for t in tracks]
    search_res = [sp.search(q=t, type='track', limit=1) for t in formatted_tracks]
    track_ids = [(first(r.get('tracks', {}).get('items', {})) or {}).get('uri') for r in search_res if
                 r.get('tracks', {}).get('items')]

    token = util.prompt_for_user_token(username, scope=scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        playlist = sp.user_playlist_create(username, playlist_name)

        if playlist and playlist.get('id'):
            sp.user_playlist_add_tracks(username, playlist.get('id'), track_ids)
            print "boom!"
    else:
        print "Can't get token for", username


@click.command()
@click.option('--subreddit', default='listentothis', help='Subreddit to get tracks from')
@click.option('--limit', default=25, help='Number of posts to fetch', type=click.IntRange(1, 50))
@click.option('--username', help='Spotify username', prompt='Please enter your Spotify username', type=str)
@click.option('--playlist_name', default='listentothis', help='Playlist name')
def subreddit_to_spotify(subreddit, limit, username, playlist_name):
    generate_spotify_playlist(get_subreddit_tracks(subreddit, limit), playlist_name, username)


if __name__ == '__main__':
    subreddit_to_spotify()
