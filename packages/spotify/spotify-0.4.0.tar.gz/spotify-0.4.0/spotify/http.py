import asyncio
import json
import random
import string
from typing import Optional, List
from base64 import b64encode
from urllib.parse import quote

import aiohttp

from .errors import HTTPException, Forbidden, NotFound, SpotifyException

__all__ = ('HTTPClient', 'HTTPUserClient', 'Route')

_GET_BEARER_ERR = '%s was `None` when getting a bearer token.'


class Route:
    """Used for constructing URLs for API endpoints.

    Parameters
    ----------
    method : str
        The HTTP/REST method used.
    path : str
        A path to be formatted.
    kwargs : Any
        The arguments to used to format the path.

    Attributes
    ----------
    path : str
        The path template.
    method : str
        The HTTP method used.
    url : str
        The formatted path.
    """
    BASE = 'https://api.spotify.com/v1'

    def __init__(self, method, path, **kwargs):
        self.path = path
        self.method = method
        self.url = (self.BASE + self.path)

        if kwargs:
            parameters = {key: (quote(v) if isinstance(v, str) else v) for key, v in kwargs.items()}
            self.url = self.url.format(**parameters)


class HTTPClient:
    """Represents an HTTP client sending HTTP requests to the Spotify API.

    Parameters
    ----------
    client_id : str
        The client id provided by spotify for the app.
    client_secret : str
        The client secret for the app.
    loop : Optional[event loop]
        The event loop the client should run on, if no loop is specified `asyncio.get_event_loop()` is called and used instead.


    Attributes
    ----------
    loop : AbstractEventLoop
        The loop the client is running with.
    client_id : str
        The client id of the app.
    client_secret : str
        The client secret.
    """
    RETRY_AMOUNT = 10

    def __init__(self, client_id, client_secret, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self._session = aiohttp.ClientSession(loop=self.loop)

        self.client_id = client_id
        self.client_secret = client_secret

        self.bearer_info = None

    async def get_bearer_info(self):
        """Get the application bearer token from client_id and client_secret."""
        if self.client_id is None:
            raise SpotifyException(_GET_BEARER_ERR % 'client_id')

        elif self.client_secret is None:
            raise SpotifyException(_GET_BEARER_ERR % 'client_secret')

        token = b64encode(':'.join((self.client_id, self.client_secret)).encode())

        kwargs = {
            'url': 'https://accounts.spotify.com/api/token',
            'data': {'grant_type': 'client_credentials'},
            'headers': {'Authorization': 'Basic ' + token.decode()}
        }

        async with self._session.post(**kwargs) as resp:
            return json.loads(await resp.text(encoding='utf-8'))

    async def request(self, route, **kwargs):
        """Make a request to the spotify API with the current bearer credentials.

        Parameters
        ----------
        route : Union[tuple[str, str], Route]
            A tuple of the method and url or a :class:`Route` object.
        kwargs : Any
            keyword arguments to pass into :class:`aiohttp.ClientSession.request`
        """
        if isinstance(route, tuple):
            method, url = route
        else:
            method = route.method
            url = route.url

        if self.bearer_info is None:
            self.bearer_info = bearer_info = await self.get_bearer_info()
            access_token = bearer_info['access_token']
        else:
            access_token = self.bearer_info['access_token']

        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': kwargs.get('content_type', 'application/json'),
            **kwargs.pop('headers', {})
        }

        for _ in range(self.RETRY_AMOUNT):
            r = await self._session.request(method, url, headers=headers, **kwargs)
            try:
                status = r.status

                try:
                    data = json.loads(await r.text(encoding='utf-8'))
                except json.decoder.JSONDecodeError:
                    data = {}

                if 300 > status >= 200:
                    return data

                if status == 401:
                    self.bearer_info = bearer_info = await self.get_bearer_info()
                    headers['Authorization'] = 'Bearer ' + bearer_info['access_token']
                    continue

                if status == 429:
                    # we're being rate limited.
                    amount = r.headers.get('Retry-After')
                    await asyncio.sleep(int(amount), loop=self.loop)
                    continue

                if status in (502, 503):
                    # unconditional retry
                    continue

                if status == 403:
                    raise Forbidden(r, data)
                elif status == 404:
                    raise NotFound(r, data)
            finally:
                await r.release()
        else:
            raise HTTPException(r, data)

    async def close(self):
        """Close the underlying HTTP session."""
        await self._session.close()

    # Methods are defined in the order that they are documented in

    # Album related endpoints

    def album(self, spotify_id: str, market: Optional[str] = 'US'):
        """Get Spotify catalog information for a single album.

        Parameters
        ----------
        spotify_id : str
            The spotify_id to search by.
        market : Optional[str]
            An ISO 3166-1 alpha-2 country code.

        Returns
        -------
        album : Dict
            The album object.
        """
        route = Route('GET', '/albums/{spotify_id}', spotify_id=spotify_id)
        payload = {}

        if market:
            payload['market'] = market

        return self.request(route, params=payload)

    def album_tracks(self, spotify_id, limit=20, offset=0, market='US'):
        """Get Spotify catalog information about an album’s tracks.

        Parameters
        ----------
        spotify_id : str
            The spotify_id to search by.
        limit : Optional[int]
            The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.
        offset : Optiona[int]
            The offset of which Spotify should start yielding from.
        market : Optional[str]
            An ISO 3166-1 alpha-2 country code.

        Returns
        -------
        tracks : List[Dict]
            The albums tracks.
        """
        route = Route('GET', '/albums/{spotify_id}/tracks', spotify_id=spotify_id)
        payload = {'limit': limit, 'offset': offset}

        if market:
            payload['market'] = market

        return self.request(route, params=payload)

    def albums(self, spotify_ids, market='US'):
        """Get Spotify catalog information for multiple albums identified by their Spotify IDs.

        Parameters
        ----------
        spotify_ids : List[str]
            The spotify_ids to search by.
        market : Optional[str]
            An ISO 3166-1 alpha-2 country code.

        Returns
        -------
        albums : List[Dict]
            The albums.
        """
        route = Route('GET', '/albums/')
        payload = {'ids': spotify_ids}

        if market:
            payload['market'] = market

        return self.request(route, params=payload)

    # Artist related endpoints.

    def artist(self, spotify_id):
        """Get Spotify catalog information for a single artist identified by their unique Spotify ID.

        Parameters
        ----------
        spotify_id : str
            The spotify_id to search by.

        Returns
        -------
        artist : Dict
            The artist requested.
        """
        route = Route('GET', '/artists/{spotify_id}', spotify_id=spotify_id)
        return self.request(route)

    def artist_albums(self, spotify_id, include_groups=None, limit=20, offset=0, market='US'):
        """Get Spotify catalog information about an artist’s albums.

        Parameters
        ----------
        spotify_id : str
            The spotify_id to search by.
        include_groups : INCLUDE_GROUPS_TP
            INCLUDE_GROUPS
        limit : Optional[int]
            The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.
        offset : Optiona[int]
            The offset of which Spotify should start yielding from.
        market : Optional[str]
            An ISO 3166-1 alpha-2 country code.

        Returns
        -------
        albums : List[Dict]
            The artists albums.
        """
        route = Route('GET', '/artists/{spotify_id}/albums', spotify_id=spotify_id)
        payload = {'limit': limit, 'offset': offset}

        if include_groups:
            payload['include_groups'] = include_groups

        if market:
            payload['market'] = market

        return self.request(route, params=payload)

    def artist_top_tracks(self, spotify_id, country):
        """Get Spotify catalog information about an artist’s top tracks by country.

        Parameters
        ----------
        spotify_id : str
            The spotify_id to search by.
        country : COUNTRY_TP
            COUNTRY

        Returns
        -------
        tracks : List[Dict]
            The artists top tracks for that country.
        """
        route = Route('GET', '/artists/{spotify_id}/top-tracks', spotify_id=spotify_id)
        payload = {'country': country}
        return self.request(route, params=payload)

    def artist_related_artists(self, spotify_id):
        """Get Spotify catalog information about artists similar to a given artist.

        Similarity is based on analysis of the Spotify community’s listening history.

        Parameters
        ----------
        spotify_id : str
            The spotify_id to search by.

        Returns
        -------
        artists : List[Dict]
            The related artists.
        """
        route = Route('GET', '/artists/{spotify_id}/related-artists', spotify_id=spotify_id)
        return self.request(route)

    def artists(self, spotify_ids):
        """Get Spotify catalog information for several artists based on their Spotify IDs.

        Parameters
        ----------
        spotify_id : List[str]
            The spotify_ids to search with.

        Returns
        -------
        artists : List[Dict]
            The artists requested.
        """
        route = Route('GET', '/artists')
        payload = {'ids': spotify_ids}
        return self.request(route, params=payload)

    # Browse endpoints.

    def category(self, category_id, country=None, locale=None):
        """Get a single category used to tag items in Spotify (on, for example, the Spotify player’s “Browse” tab).

        Parameters
        ----------
        category_id : str
            The Spotify category ID for the category.
        country : COUNTRY_TP
            COUNTRY
        locale : LOCALE_TP
            LOCALE

        Returns
        -------
        category : Dict
            The category object.
        """
        route = Route('GET', '/browse/categories/{category_id}', category_id=category_id)
        payload = {}

        if country:
            payload['country'] = country

        if locale:
            payload['locale'] = locale

        return self.request(route, params=payload)

    def category_playlists(self, category_id, limit=20, offset=0, country=None):
        """Get a list of Spotify playlists tagged with a particular category.

        Parameters
        ----------
        category_id : str
            The Spotify category ID for the category.
        limit : Optional[int]
            The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.
        offset : Optional[int]
            The index of the first item to return. Default: 0
        country : COUNTRY_TP
            COUNTRY

        Returns
        -------
        playlists : Dict
            A list of simple playlist objects wrapped in a paging object.
        """
        route = Route('GET', '/browse/categories/{category_id}/playlists', category_id=category_id)
        payload = {'limit': limit, 'offset': offset}

        if country:
            payload['country'] = country

        return self.request(route, params=payload)

    def categories(self, limit=20, offset=0, country=None, locale=None):
        """Get a list of categories used to tag items in Spotify (on, for example, the Spotify player’s “Browse” tab).

        Parameters
        ----------
        limit : Optional[int]
            The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.
        offset : Optional[int]
            The index of the first item to return. Default: 0
        country : COUNTRY_TP
            COUNTRY
        locale : LOCALE_TP
            LOCALE

        Returns
        -------
        categories : Dict
            A list of category objects wrapped in a paging object.
        """
        route = Route('GET', '/browse/categories')
        payload = {'limit': limit, 'offset': offset}

        if country:
            payload['country'] = country

        if locale:
            payload['locale'] = locale

        return self.request(route, params=payload)

    def featured_playlists(self, locale=None, country=None, timestamp=None, limit=20, offset=0):
        """Get a list of Spotify featured playlists (shown, for example, on a Spotify player’s ‘Browse’ tab).

        Parameters
        ----------
        locale : LOCALE_TP
            LOCALE
        country : COUNTRY_TP
            COUNTRY
        timestamp : TIMESTAMP_TP
            TIMESTAMP
        limit : Optional[int]
            The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.
        offset : Optional[int]
            The index of the first item to return. Default: 0

        Returns
        -------
        featured : Dict
            The returned object has a `playlist` field with a list of simple playlist objects.
            additionally there is a `message` field.
        """
        route = Route('GET', '/browse/featured-playlists')
        payload = {'limit': limit, 'offset': offset}

        if country:
            payload['country'] = country

        if locale:
            payload['locale'] = locale

        if timestamp:
            payload['timestamp'] = timestamp

        return self.request(route, params=payload)

    def new_releases(self, *, country=None, limit=20, offset=0):
        """Get a list of new album releases featured in Spotify (shown, for example, on a Spotify player’s “Browse” tab).

        Parameters
        ----------
        limit : Optional[int]
            The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.
        offset : Optional[int]
            The index of the first item to return. Default: 0
        country : COUNTRY_TP
            COUNTRY

        Returns
        -------
        releases : Dict
            A paging object of simple album objects.
        """
        route = Route('GET', '/browse/new-releases')
        payload = {'limit': limit, 'offset': offset}

        if country:
            payload['country'] = country

        return self.request(route, params=payload)

    def recommendations(self, seed_artists, seed_genres, seed_tracks, *, limit=20, market=None, **filters):
        """Get Recommendations Based on Seeds.

        Parameters
        ----------
        seed_artists : str
            A comma separated list of Spotify IDs for seed artists. Up to 5 seed values may be provided.
        seed_genres : str
            A comma separated list of any genres in the set of available genre seeds. Up to 5 seed values may be provided.
        seed_tracks : str
            A comma separated list of Spotify IDs for a seed track. Up to 5 seed values may be provided.
        limit : Optional[int]
            The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.
        market : Optional[str]
            An ISO 3166-1 alpha-2 country code.
        max_* : Optional[Keyword arguments]
            For each tunable track attribute, a hard ceiling on the selected track attribute’s value can be provided.
        min_* : Optional[Keyword arguments]
            For each tunable track attribute, a hard floor on the selected track attribute’s value can be provided.
        target_* : Optional[Keyword arguments]
            For each of the tunable track attributes (below) a target value may be provided.

        Returns
        -------
        recommendations : Dict
            A recommendations object.
        """
        route = Route('GET', '/recommendations')
        payload = {'seed_artists': seed_artists, 'seed_genres': seed_genres, 'seed_tracks': seed_tracks, 'limit': limit}

        if market:
            payload['market'] = market

        if filters:
            payload.update(filters)

        return self.request(route, param=payload)

    # Follow related endpoints.

    def following_artists_or_users(self, ids, *, type='artist'):
        """Check to see if the current user is following one or more artists or other Spotify users.

        Parameters
        ----------
        ids : List[str]
            A comma-separated list of the artist or the user Spotify IDs to check.
            A maximum of 50 IDs can be sent in one request.
        type : Optional[str]
            The ID type: either "artist" or "user".
            Default: "artist"

        Returns
        -------

        """
        route = Route('GET', '/me/following/contains')
        payload = {'ids': ids, 'type': type}

        return self.request(route, params=payload)

    def following_playlists(self, owner_id, playlist_id, *, ids):
        """
        """
        route = Route('GET', '/users/{owner_id}/playlists/{playlist_id}/followers/contains', owner_id=owner_id, playlist_id=playlist_id)
        payload = {'ids': ids}

        return self.request(route, params=payload)

    def follow_artist_or_user(self, ids, *, type='artist'):
        """Add the current user as a follower of one or more artists or other Spotify users.

        Parameters
        ----------
        ids : List[str]
            A comma-separated list of the artist or the user Spotify IDs to check.
            A maximum of 50 IDs can be sent in one request.
        type : Optional[str]
            The ID type: either "artist" or "user".
            Default: "artist"

        Returns
        -------

        """
        route = Route('PUT', '/me/following')
        payload = {'ids': ids, 'type': type}

        return self.request(route, params=payload)

    def follow_playlist(self, owner_id, playlist_id, *, public=False):
        """
        """
        route = Route('PUT', '/users/{owner_id}/playlists/{playlist_id}/followers', owner_id=owner_id, playlist_id=playlist_id)

        content = json.dumps({'public': public})

        return self.request(route, content=content)

    def followed_artists(self, limit=20, after=None):
        route = Route('GET', '/me/following')
        payload = {'limit': limit, 'type': 'artist'}

        if after:
            payload['after'] = after

        return self.request(route, params=payload)

    def unfollow_artists_or_users(self, ids, *, type='artist'):
        route = Route('DELETE', '/me/following')
        payload = {'ids': ids, 'type': type}

        return self.request(route, params=payload)

    def unfollow_playlist(self, owner_id, playlist_id):
        route = Route('DELETE', '/users/{owner_id}/playlists/{playlist_id}/followers', owner_id=owner_id, playlist_id=playlist_id)

        return self.request(route)

    def is_saved_album(self, ids):
        route = Route('GET', '/me/albums/contains')
        payload = {'ids': ids}

        return self.request(route, params=payload)

    def is_saved_track(self, ids):
        route = Route('GET', '/me/tracks/contains')
        payload = {'ids': ids}

        return self.request(route, params=payload)

    def saved_albums(self, *, limit=20, offset=0, market=None):
        route = Route('GET', '/me/albums')
        payload = {'limit': limit, 'offset': offset}

        if market:
            payload['market'] = market

        return self.request(route, params=payload)

    def saved_tracks(self, *, limit=20, offset=0, market=None):
        route = Route('GET', '/me/tracks')
        payload = {'limit': limit, 'offset': offset}

        if market:
            payload['market'] = market

        return self.request(route, params=payload)

    def delete_saved_albums(self, ids):
        route = Route('DELETE', '/me/albums')
        payload = {'ids': ids}

        return self.request(route, params=payload)

    def delete_saved_tracks(self, ids):
        route = Route('DELETE', '/me/tracks')
        payload = {'ids': ids}

        return self.request(route, params=payload)

    def save_tracks(self, ids):
        route = Route('PUT', '/me/tracks')
        payload = {'ids': ids}

        return self.request(route, params=payload)

    def save_albums(self, ids):
        route = Route('PUT', '/me/albums')
        payload = {'ids': ids}

        return self.request(route, params=payload)

    def top_artists_or_tracks(self, type, *, limit=20, offset=0, time_range=None):
        route = Route('GET', '/me/top/{type}', type=type)
        payload = {'limit': limit, 'offset': offset}

        if time_range:
            payload['time_range'] = time_range

        return self.request(route)

    def available_devices(self):
        route = Route('GET', '/me/player/devices')
        return self.request(route)

    def current_player(self, *, market=None):
        route = Route('GET', '/me/player')
        payload = {}

        if market:
            payload['market'] = market

        return self.request(route, params=payload)

    def recently_played(self, *, limit=20, before=None, after=None):
        route = Route('GET', '/me/player/recently-played')
        payload = {'limit': limit}

        if before:
            payload['before'] = before
        elif after:
            payload['after'] = after

        return self.request(route, params=payload)

    def currently_playing(self, *, market=None):
        route = Route('GET', '/me/player/currently-playing')
        payload = {}

        if market:
            payload['market'] = market

        return self.request(route, params=payload)

    def pause_playback(self, *, device_id=None):
        route = Route('PUT', '/me/player/pause')
        payload = {}

        if device_id:
            payload['device_id'] = device_id

        return self.request(route, params=payload)

    def seek_playback(self, position_ms, *, device_id=None):
        route = Route('PUT', '/me/player/seek')
        payload = {'position_ms': position_ms}

        if device_id:
            payload['device_id'] = device_id

        return self.request(route, params=payload)

    def repeat_playback(self, state, *, device_id=None):
        route = Route('PUT', '/me/player/repeat')
        payload = {'state': state}

        if device_id:
            payload['device_id'] = device_id

        return self.request(route, params=payload)

    def set_playback_volume(self, volume, *, device_id=None):
        route = Route('PUT', '/me/player/volume')
        payload = {'volume_percent': volume}

        if device_id:
            payload['device_id'] = device_id

        return self.request(route, params=payload)

    def skip_next(self, *, device_id=None):
        route = Route('POST', '/me/player/next')
        payload = {}

        if device_id:
            payload['device_id'] = device_id

        return self.request(route, params=payload)

    def skip_previous(self, *, device_id=None):
        route = Route('POST', '/me/player/previous')
        payload = {}

        if device_id:
            payload['device_id'] = device_id

        return self.request(route, params=payload)

    def play_playback(self, context_uri, *, offset=None, device_id=None):
        route = Route('PUT', '/me/player/play')
        payload = {}

        if isinstance(context_uri, str):
            payload['context_uri'] = {'context_uri': context_uri}

        elif context_uri is not None:
            payload['uris'] = {'uris': list(*context_uri)}

        else:
            pass  # Raise here?

        if offset:
            payload['offset'] = offset

        if device_id:
            payload['device_id'] = device_id

        return self.request(route, data=json.dumps(payload))

    def shuffle_playback(self, state, *, device_id=None):
        route = Route('PUT', '/me/player/seek')
        payload = {'state': state}

        if device_id:
            payload['device_id'] = device_id

        return self.request(route, params=payload)

    def transfer_player(self, device_id, *, play=None):
        route = Route('PUT', '/me/player')
        payload = {'device_ids': [device_id]}

        if play:
            payload['play'] = play

        return self.request(route, data=json.dumps(payload))

    def add_playlist_tracks(self, user_id, playlist_id, tracks, *, position=None):
        route = Route('POST', '/users/{user_id}/playlists/{playlist_id}/tracks', user_id=user_id, playlist_id=playlist_id)
        payload = {'uris': tracks}

        if position:
            payload['position'] = position

        return self.request(route, params=payload)

    def change_playlist_details(self, user_id, playlist_id, *, data):
        route = Route('PUT', '/users/{user_id}/playlists/{playlist_id}/tracks', user_id=user_id, playlist_id=playlist_id)
        return self.request(route, data=json.dumps(data))

    def create_playlist(self, user_id, *, data):
        route = Route('POST', '/users/{user_id}/playlists', user_id=user_id)
        return self.request(route, data=json.dumps(data))

    def current_playlists(self, *, limit=20, offset=0):
        route = Route('GET', '/me/playlists')
        return self.request(route, params={'limit': limit, 'offset': offset})

    def get_playlists(self, user_id, *, limit=20, offset=0):
        route = Route('GET', '/users/{user_id}/playlists', user_id=user_id)
        return self.request(route, params={'limit': limit, 'offset': offset})

    def get_playlist_cover_image(self, user_id, playlist_id):
        route = Route('GET', '/users/{user_id}/playlists/{playlist_id}/images', user_id=user_id, playlist_id=playlist_id)
        return self.request(route)

    def get_playlist(self, user_id, playlist_id, *, fields=None, market=None):
        route = Route('GET', '/users/{user_id}/playlists/{playlist_id}', user_id=user_id, playlist_id=playlist_id)
        payload = {}

        if fields:
            payload['fields'] = fields

        if market:
            payload['market'] = market

        return self.request(route, params=payload)

    def get_playlist_tracks(self, user_id, playlist_id, *, fields=None, market=None, limit=20, offset=0):
        route = Route('GET', '/users/{user_id}/playlists/{playlist_id}/tracks', user_id=user_id, playlist_id=playlist_id)
        payload = {'limit': limit, 'offset': offset}

        if fields:
            payload['fields'] = fields

        if market:
            payload['market'] = market

        return self.request(route, params=payload)

    def remove_playlist_tracks(self, user_id, playlist_id, tracks, *, position=None, snapshot_id=None):
        route = Route('DELETE ', '/users/{user_id}/playlists/{playlist_id}/tracks', user_id=user_id, playlist_id=playlist_id)
        payload = {'uris': tracks}

        if position:
            payload['position'] = position

        if snapshot_id:
            payload['snapshot_id'] = snapshot_id

        return self.request(route, params=payload)

    def reorder_playlists_tracks(self, user_id, playlist_id, range_start, range_length, insert_before, *, snapshot_id=None):
        route = Route('PUT', '/users/{user_id}/playlists/{playlist_id}/tracks', user_id=user_id, playlist_id=playlist_id)
        payload = {'range_start': range_start, 'range_length': range_length, 'insert_before': insert_before}

        if snapshot_id:
            payload['snapshot_id'] = snapshot_id

        return self.request(route, data=payload)

    def replace_playlist_tracks(self, user_id, playlist_id, tracks):
        route = Route('PUT', '/users/{user_id}/playlists/{playlist_id}/tracks', user_id=user_id, playlist_id=playlist_id)
        payload = {'uris': tracks}

        return self.request(route, params=payload)

    def upload_playlist_cover_image(self, user_id, playlist_id, file):
        route = Route('PUT', '/users/{user_id}/playlists/{playlist_id}/images', user_id=user_id, playlist_id=playlist_id)
        return self.request(route, data=b64encode(file.read()), content_type='image/jpeg')

    def track_audio_analysis(self, track_id):
        route = Route('GET', '/audio-analysis/{id}', id=track_id)
        return self.request(route)

    def track_audio_features(self, track_id):
        route = Route('GET', '/audio-features/{id}', id=track_id)
        return self.request(route)

    def audio_features(self, track_ids):
        route = Route('GET', '/audio-features')
        return self.request(route, params={'ids': track_ids})

    def track(self, track_id):
        route = Route('GET', '/tracks/{id}', id=track_id)
        return self.request(route)

    def tracks(self, track_ids):
        route = Route('GET', '/tracks')
        return self.request(route, params={'ids': track_ids})

    def current_user(self):
        route = Route('GET', '/me')
        return self.request(route)

    def user(self, user_id):
        route = Route('GET', '/users/{user_id}', user_id=user_id)
        return self.request(route)

    def search(self, q, queary_type='track,playlist,artist,album', market='US', limit=20, offset=0):
        route = Route('GET', '/search')
        payload = {'q': q, 'type': queary_type, 'limit': limit, 'offset': offset}

        if market:
            payload['market'] = market

        return self.request(route, params=payload)


class HTTPUserClient(HTTPClient):
    """HTTPClient for access to user endpoints."""
    def __init__(self, token, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self._session = aiohttp.ClientSession(loop=self.loop)

        self.bearer_info = {'access_token': token}
        self.token = token

    async def get_bearer_info(self):
        return {'access_token': self.token}
