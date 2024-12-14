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

    c1,c2 = st.columns((1,1))

    #---------- Artist Tables ----------

    c1.subheader('Most listened artists')

    df_artists = get_most_listened_artists(df, mode='minutes')
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

    df_artists_no1 = get_most_no1_artists(df)
    fig_a_1 = go.Figure(data=[go.Table(
        header=dict(values=list(df_artists_no1.columns),
                    fill_color=DARK_GREEN,
                    font=dict(size=12, color = 'white'),
                    align='left'),
        cells=dict(values=df_artists_no1.transpose().values.tolist(),
                font=dict(size=12, color = 'black'),
                align='left'))
    ])
    fig_a_1.update_layout(table_layout)

    c1.plotly_chart(fig_a, use_container_width=True, key='table_artists')
    c1.plotly_chart(fig_a_1, use_container_width=True, key='table_artists_no1')

    #---------- Song Tables ----------

    c2.subheader('Most listened songs')

    df_songs = get_most_listened_songs(df, mode='minutes')
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

    df_songs_no1 = get_most_no1_songs(df)
    fig_s_1 = go.Figure(data=[go.Table(
        header=dict(values=list(df_songs_no1.columns),
                    fill_color=DARK_GREEN,
                    font=dict(size=12, color = 'white'),
                    align='left'),
        cells=dict(values=df_songs_no1.transpose().values.tolist(),
                font=dict(size=12, color = 'black'),
                align='left'))
    ])
    fig_s_1.update_layout(table_layout)

    c2.plotly_chart(fig_s, use_container_width=True, key='table_songs')
    c2.plotly_chart(fig_s_1, use_container_width=True, key='table_songs_no1')

    #---------- Weekly Evolution Graph ----------

    d1,d2,d3 = st.columns((0.3,0.3,0.5))

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
        "Write/Select Song Name (Filtered by Artist)",
        options=[""] + list(filtered_songs),
        format_func=lambda x: "" if x == "" else x,
    )

    if selected_artist and selected_song:
        filtered_df = df[(df["artist"] == selected_artist) & (df["track"] == selected_song)]
    elif selected_artist:
        filtered_df = df[df["artist"] == selected_artist]
    else:
        filtered_df = pd.DataFrame()

    if not filtered_df.empty:

        grouped_df = filtered_df.groupby(["calendar_week"]).agg({"minutes": "sum"}).sort_values("calendar_week").reset_index()

        all_weeks = pd.period_range(start=grouped_df['calendar_week'].min(), end=grouped_df['calendar_week'].max(), freq='W')
        all_weeks_df = pd.DataFrame(all_weeks, columns=['calendar_week'])

        grouped_df = all_weeks_df.merge(grouped_df, on='calendar_week', how='left')
        grouped_df["minutes"] = grouped_df["minutes"].fillna(0)
        grouped_df["calendar_week"] = grouped_df["calendar_week"].astype(str)

        fig = px.line(
            grouped_df,
            x="calendar_week",
            y="minutes",
            title=f"Streamed Minutes per Week for {selected_artist} - {selected_song if selected_song else 'All Songs'}",
            markers=True,
        )
        fig.update_layout(
            xaxis_title="Calendar Week",
            yaxis_title="Streamed Minutes",
            template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True)