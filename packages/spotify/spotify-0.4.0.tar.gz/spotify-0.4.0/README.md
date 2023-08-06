![logo](logo.png)


![Version info](https://img.shields.io/pypi/v/spotify.svg)
[![GitHub stars](https://img.shields.io/github/stars/mental32/spotify.py.svg)](https://github.com/mental32/spotify.py/stargazers)
![Discord](https://img.shields.io/discord/438465139197607939.svg?style=flat-square)

# spotify.py

An API library for the spotify client and the Spotify Web API written in Python.

Spotify.py is an, primarily, asyncronous library (everything down to the HTTP client is asyncio friendly). 
The library also supports **syncronous** usage with `spotify.sync`

```python
import spotify.sync as spotify  # Nothing requires async/await now!
```

## example

- Top tracks (drake)

```py
import spotify

client = spotify.Client('someid', 'sometoken')

async def example():
    drake = await client.get_artist('3TVXtAsR1Inumwj472S9r4')

    for track in await drake.top_tracks():
        print(repr(track))
```

## Installing

To install the library simply clone it and run setup.py
- `git clone https://github.com/mental32/spotify.py`
- `python3 setup.py install`

or use pypi

- `pip3 install spotify` (latest stable)
- `pip3 install -U git+https://github.com/mental32/spotify.py` (nightly)

## Resources

For resources look at the [examples](https://github.com/mental32/spotify.py/tree/master/examples) or ask in the [discord](https://discord.gg/k43FSFF)
