import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from src.data_processing import create_clean_dataframe
from src.stats import get_most_listened_artists, get_most_listened_songs, get_most_no1_artists, get_most_no1_songs

from configurations.streamlit_config import table_layout

DARK_GREEN = '#022100'

df = create_clean_dataframe('data/songs_1.json')


st.set_page_config(page_title='Personal Spotify',  layout='wide', page_icon=':microphone:')

st.title('Personal Spotify Wrapped')

c1,c2 = st.columns((1,1))

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