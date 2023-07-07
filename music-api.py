import json
from spotify import *
from text_miner import *

def hello(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def get_user_playlists(event, context):
    # variables
    songs = []
    username = 12125327174 # --> JowMao () --> event['username']
    helper = spotifyApi()
    sp = helper.sp
    playlists = helper.get_user_playlists(username=username, sp=sp)
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": playlists,
    }
    for playlist in tqdm(playlists):
        # retrieve playlist songs
        tracklist = helper.get_playlist_content(username=username, playlist=playlist, sp=sp, csv=False)
        
        # retrieve playlist audio features
        tmp_df = helper.get_playlist_audio_features(username=username, playlist=playlist, sp=sp, csv=False)
        audio_df = pd.concat([audio_df, tmp_df], axis=0)
        
        # retrieve song lyrics (searching genius api)
        for track in tracklist:
            track['genius_url'] = None
            track_name = track["track"]["name"]
            track_artist = track["track"]["artists"][0]["name"]
            genius_song_info = txtMiner.search_genius_song(track_name=track_name, track_artist=track_artist, debug=False)
            if genius_song_info:
                track["track"]["genius_info"] = genius_song_info
            else:
                track["track"]["genius_info"] = {
                    "result": {
                        "url": "https://genius.com/" + track_name.replace(" ", "-") + "-" + track_artist.replace(" ", "-") + "-" + "lyrics"
                    }
                }
            track["track"]["lyrics"] = txtMiner.scrape_genius_lyrics(artistname=track_artist, songname=track_name, url=track["track"]["genius_info"]["result"]["url"])
    
        # save collected data for tracklist
        songs.extend(tracklist)
    
    print(
        f"\nExtracted {len(songs)} songs from {len(playlists)} playlists from your Spotify Account.\nScraped lyrics for {len([s for s in songs if s['track']['lyrics'] != ''])} of the {len(songs)} songs from genius.com."
    )

    # savings objects here just in case...
    txtMiner.save_df(filename=f"User_{username}_audioFeautures_", df=audio_df)
    txtMiner.save_df(filename=f"User_{username}_songsNlyrics_", df=pd.DataFrame([songs]))

    response = {"statusCode": 200, "body": json.dumps(body)}
    return response






