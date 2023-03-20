import streamlit as st
from datetime import datetime, date
import GBG_Pingis as util
import matplotlib.pyplot as plt
import altair as alt



#%%
conn = util.get_db_conn()
st.title("Matchstatistik")

matches = util.get_outcomes_table(conn)
# players = util.get_player_table(conn)


st.write('### Spelade matcher per dag')
matches_per_date = matches.drop(columns=['player', 'opponent', 'win_or_lose', 'win_score', 'lose_score', 'elo'])
matches_per_date = matches_per_date.rename(columns={'gametime': 'matcher'}).groupby('gamedate', as_index=False).count()
matches_per_date = matches_per_date.astype({'gamedate': str})
matches_per_date['matcher'] = matches_per_date['matcher'].apply(lambda number: int(number/2))
matches_per_date = alt.Chart(matches_per_date).mark_bar().encode(x='gamedate', y='matcher')
st.altair_chart(matches_per_date)


st.write('### Spelaraktivitet')
player_activity = matches[['player', 'elo']].groupby('player', as_index=False).count()
player_activity = player_activity.rename(columns={'elo': 'matcher'})
player_activity = player_activity.sort_values(by=['matcher']).reset_index(drop=True)

player_activity = alt.Chart(player_activity).mark_bar().encode(x=alt.X('player', sort=None), y='matcher')
st.altair_chart(player_activity)


conn.close()
