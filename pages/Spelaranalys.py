import streamlit as st
from datetime import datetime, date
import GBG_Pingis as util
import matplotlib.pyplot as plt
import numpy as np


#%%
conn = util.get_db_conn()
st.title("Spelaranalys")

matches = util.get_outcomes_table(conn)
players = util.get_player_table(conn)
players = players[players['name']!='Välj vinnare']
players = players[players['name']!='Välj förlorare']

player = st.selectbox('Välj spelare', players['name'])
if (player != '') and len(matches[matches['player']==player]) > 0:

    matches = matches[matches['player']==player].drop(columns=['player', 'gamedate'])

    st.write('### Siffror')
    left_column, right_column, righter_column = st.columns(3)
    with left_column:
        win_rate = len(matches[matches['win_or_lose']=='winner']) / len(matches)
        st.write('Win rate:', win_rate*100, '%')
    with right_column:
        st.write('Lose rate:', (1-win_rate)*100, '%')
    with righter_column:
        avg_elo = matches['elo'].mean()
        st.write('Medel-elo:', avg_elo)


    st.write('### Elo time evolution')
    st.line_chart(matches, x='gametime', y='elo')

    st.write('### Dina bästa och värsta motståndare')
    st.write('(Lång positiv stapel = svårt motstånd, Lång negativ stapel = Lätt motstånd)')

    matches['my_score'] = np.where(matches['win_or_lose']=='winner', matches['win_score'], matches['lose_score'])
    matches['op_score'] = np.where(matches['win_or_lose']=='loser', matches['win_score'], matches['lose_score'])
    scores_by_op = matches.drop(columns=['gametime', 'win_score', 'lose_score', 'win_or_lose', 'elo']).groupby('opponent', as_index=False).sum()
    scores_by_op['score_diff'] = scores_by_op['op_score'] - scores_by_op['my_score']
    st.bar_chart(scores_by_op, x='opponent', y='score_diff')
    
    st.write('### Dina spelade matcher')
    st.write(matches.drop(columns=['win_score', 'lose_score']))



conn.close()
