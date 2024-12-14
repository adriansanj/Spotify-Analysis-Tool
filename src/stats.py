# Description: This file contains functions to get statistics from the data.

def get_most_listened_artists(df, mode = "minutes"):
    
    if mode == "count":
        most_listened_artists = df.groupby(['artist']).size().sort_values(ascending=False).reset_index().rename(columns={0: 'count'})
    else:
        most_listened_artists = df.groupby(['artist'])['minutes'].sum().reset_index().sort_values('minutes', ascending=False)
    
    return most_listened_artists


def get_most_listened_songs(df, mode = "minutes"):

    if mode == "count":
        most_listened_songs= df.groupby(['artist', 'track']).size().sort_values(ascending=False).reset_index().rename(columns={0: 'count'})
    
    else:
        most_listened_songs = df.groupby(['track', 'artist'])['minutes'].sum().reset_index().sort_values('minutes', ascending=False)
        
    return most_listened_songs

#TODO Aggregations
def get_most_no1_artists(df, agg = 'day'):
    artist_daily_plays = df.groupby([agg, 'artist'])['minutes'].sum().reset_index()
    most_streamed_per_day = artist_daily_plays.loc[artist_daily_plays.groupby(agg)['minutes'].idxmax()]
    most_streamed_per_day_count = most_streamed_per_day.groupby('artist').size().sort_values(ascending=False).reset_index().rename(columns={0: f'{agg}s at 1'})

    return most_streamed_per_day_count

def get_most_no1_songs(df, agg = 'day'):
    song_daily_plays = df.groupby([agg, 'track', 'artist'])['minutes'].sum().reset_index()
    most_streamed_per_day = song_daily_plays.loc[song_daily_plays.groupby(agg)['minutes'].idxmax()]
    most_streamed_per_day_count = most_streamed_per_day.groupby(['track', 'artist']).size().sort_values(ascending=False).reset_index().rename(columns={0: f'{agg}s at 1'})

    return most_streamed_per_day_count
    
