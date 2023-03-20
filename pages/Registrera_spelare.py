import pandas as pd
import numpy as np
import os
import streamlit as st

import GBG_Pingis as util


#%%
conn = util.get_db_conn()
st.title("Registrera spelare")

done = False
if not done:

    players = util.get_player_table(conn)
    st.text_input("Ditt namn", value='', key="name")
    if st.session_state.name != '':

        if st.session_state.name in set(players['name'].values):
            st.warning("Spelaren finns redan")

        else:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO players (player, matches, wins, losses, elo) VALUES (%s, 0, 0, 0, %s)', (st.session_state.name, util.START_ELO))
                st.success(f"Spelaren {st.session_state.name} registrerad")
            done = True

else:
    st.write("Ladda om sidan för att registrera igen")

conn.close()

