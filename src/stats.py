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

def get_most_listened_artist_table(df):
    df_artists = get_most_listened_artists(df, mode='minutes')
    df_artists_no1_days = get_most_no1_artists(df)
    df_artists_no1_weeks = get_most_no1_artists(df, agg='week')
    df_artists_no1_months = get_most_no1_artists(df, agg='month')   
    df_artists = df_artists.merge(df_artists_no1_days, on='artist', how='left')
    df_artists = df_artists.merge(df_artists_no1_weeks, on='artist', how='left')
    df_artists = df_artists.merge(df_artists_no1_months, on='artist', how='left')
    df_artists = df_artists.fillna(0).reset_index(drop=False)
    df_artists['index'] = df_artists['index'] + 1

    return df_artists

def get_most_listened_songs_table(df):
    df_songs = get_most_listened_songs(df, mode='minutes')
    df_songs_no1_days = get_most_no1_songs(df)
    df_songs_no1_weeks = get_most_no1_songs(df, agg='week')
    df_songs_no1_months = get_most_no1_songs(df, agg='month')   
    df_songs = df_songs.merge(df_songs_no1_days, on=['track','artist'], how='left')
    df_songs = df_songs.merge(df_songs_no1_weeks, on=['track','artist'], how='left')
    df_songs = df_songs.merge(df_songs_no1_months, on=['track','artist'], how='left')
    df_songs = df_songs.fillna(0).reset_index(drop=False)
    df_songs['index'] = df_songs['index'] + 1
    
    return df_songs
