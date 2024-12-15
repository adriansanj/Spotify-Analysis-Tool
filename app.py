import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


from src.data_processing import create_clean_dataframe
from src.stats import get_most_listened_artists, get_most_listened_songs, get_most_no1_artists, get_most_no1_songs

from configurations.streamlit_config import table_layout
import os

DARK_GREEN = '#022100'

# data_files = [f for f in os.listdir('data') if f.endswith('.json')]
# df = create_clean_dataframe(data_files)

st.set_page_config(page_title='Personal Spotify',  layout='wide', page_icon=':microphone:')

st.title('Personal Spotify Wrapped')

uploaded_files = st.file_uploader("Upload extended streaming history json files", help="Drag and drop doesn't work properly", accept_multiple_files=True)

if uploaded_files:
    data_files = [f for f in uploaded_files]
    df = create_clean_dataframe(data_files)

    st.markdown("---")

    st.write("### Filter Data by Date")
    a1,a2,a3 = st.columns((0.1,0.1,1))
    
    min_time = df["timestamp"].min()
    max_time = df["timestamp"].max()

    # Streamlit slider for time range selection
    start_date = a1.date_input("Start date:", value=min_time.to_pydatetime().date(), min_value=min_time.to_pydatetime().date(), max_value=max_time.to_pydatetime().date())
    end_date = a2.date_input("End date:", value=max_time.to_pydatetime().date(), min_value=min_time.to_pydatetime().date(), max_value=max_time.to_pydatetime().date())

    df = df[(df["timestamp"] >= pd.Timestamp(start_date, tz="UTC")) & 
                     (df["timestamp"] <= pd.Timestamp(end_date, tz="UTC"))]
    
    st.markdown("---")

    h1,h2,h3 = st.columns((1,1,1))

    
    # Total Minutes Played
    h1.markdown(f"### :musical_note: **Total Minutes Played**")
    h1.write(f"**{df['minutes'].sum():,.0f} minutes**")

    # Unique Artists Played
    h2.markdown(f"### :star: **Unique Artists Played**")
    h2.write(f"**{df['artist'].nunique()} artists**")

    # Unique Songs Played
    h3.markdown(f"### :headphones: **Unique Songs Played**")
    h3.write(f"**{df['track'].nunique()} songs**")

    st.markdown("---")

    c1,c2 = st.columns((1,1))

    #---------- Artist Tables ----------

    c1.subheader('Most listened artists')

    df_artists = get_most_listened_artists(df, mode='minutes')
    df_artists_no1_days = get_most_no1_artists(df)
    df_artists_no1_weeks = get_most_no1_artists(df, agg='week')
    df_artists_no1_months = get_most_no1_artists(df, agg='month')   
    df_artists = df_artists.merge(df_artists_no1_days, on='artist', how='left')
    df_artists = df_artists.merge(df_artists_no1_weeks, on='artist', how='left')
    df_artists = df_artists.merge(df_artists_no1_months, on='artist', how='left')
    df_artists = df_artists.fillna(0).reset_index(drop=False)
    df_artists['index'] = df_artists['index'] + 1

    fig_a = go.Figure(data=[go.Table(
        header=dict(values=list(df_artists.columns),
                    fill_color=DARK_GREEN,
                    font=dict(size=12, color = 'white'),
                    align='left'),
        cells=dict(values=df_artists.transpose().values.tolist(),
                font=dict(size=12, color = 'black'),
                align='left'))
    ])
    fig_a.update_layout(table_layout)

    

    c1.plotly_chart(fig_a, use_container_width=True, key='table_artists')

    #---------- Song Tables ----------

    c2.subheader('Most listened songs')

    df_songs = get_most_listened_songs(df, mode='minutes')
    df_songs_no1_days = get_most_no1_songs(df)
    df_songs_no1_weeks = get_most_no1_songs(df, agg='week')
    df_songs_no1_months = get_most_no1_songs(df, agg='month')   
    df_songs = df_songs.merge(df_songs_no1_days, on=['track','artist'], how='left')
    df_songs = df_songs.merge(df_songs_no1_weeks, on=['track','artist'], how='left')
    df_songs = df_songs.merge(df_songs_no1_months, on=['track','artist'], how='left')
    df_songs = df_songs.fillna(0).reset_index(drop=False)
    df_songs['index'] = df_songs['index'] + 1

    fig_s = go.Figure(data=[go.Table(
        header=dict(values=list(df_songs.columns),
                    fill_color=DARK_GREEN,
                    font=dict(size=12, color = 'white'),
                    align='left'),
        cells=dict(values=df_songs.transpose().values.tolist(),
                font=dict(size=12, color = 'black'),
                align='left'))
    ])
    fig_s.update_layout(table_layout)


    
    

    c2.plotly_chart(fig_s, use_container_width=True, key='table_songs')
    # with c2:
    #     AgGrid(df_songs, sortable=True)
    st.markdown("---")
    #---------- Weekly Evolution Graph ----------

    d1,d2,d3,d4,d5 = st.columns((0.3,0.3,0.1,0.3,0.3))
    
    # Artist Search Input
    selected_artist = d1.selectbox(
        "Write/Select Artist Name",
        options=[""] + list(df["artist"].unique()),
        format_func=lambda x: "" if x == "" else x,
    )

    # Filter songs based on selected artist
    if selected_artist:
        filtered_songs = df[df["artist"] == selected_artist]["track"].unique()
    else:
        filtered_songs = [] 

    # Song Search Input
    selected_song = d2.selectbox(
        "Write/Select Song Name",
        options=[""] + list(filtered_songs),
        format_func=lambda x: "" if x == "" else x,
    )

    if selected_artist and selected_song:
        filtered_df = df[(df["artist"] == selected_artist) & (df["track"] == selected_song)]
    elif selected_artist:
        filtered_df = df[df["artist"] == selected_artist]
    else:
        filtered_df = pd.DataFrame()

    if selected_artist:
        # Total Minutes Played
        d4.markdown(f":musical_note: **Total Minutes Played**")
        d4.write(f"**{filtered_df['minutes'].sum():,.0f} minutes**")

        # Unique Songs Played
        d5.markdown(f":headphones: **Unique Songs Played**")
        d5.write(f"**{filtered_df['track'].nunique()} songs**")


    if not filtered_df.empty:

        grouped_df = filtered_df.groupby(["week"]).agg({"minutes": "sum"}).sort_values("week").reset_index()

        all_weeks = pd.period_range(start=grouped_df['week'].min(), end=grouped_df['week'].max(), freq='W')
        all_weeks_df = pd.DataFrame(all_weeks, columns=['week'])

        grouped_df = all_weeks_df.merge(grouped_df, on='week', how='left')
        grouped_df["minutes"] = grouped_df["minutes"].fillna(0)
        grouped_df["week"] = grouped_df["week"].astype(str)

        fig = px.line(
            grouped_df,
            x="week",
            y="minutes",
            title=f"Streamed Minutes per Week for {selected_artist} - {selected_song if selected_song else 'All Songs'}",
            markers=True,
        )
        fig.update_layout(
            xaxis_title="Calendar Week",
            yaxis_title="Streamed Minutes",
            template="plotly_white",
            xaxis=dict(
                tickangle=-45,  # Rotate the x-axis labels to avoid overlap
                tickfont=dict(size=10),  # Adjust the font size for the x-axis labels
            ),
        )
        st.plotly_chart(fig, use_container_width=True)