import streamlit as st
from datetime import datetime, date
import GBG_Pingis as util


def register_game(conn, gametime, player, opponent, win_or_lose, win_score, lose_score, elo):
    gamedate = str(date.today())

    with conn.cursor() as cursor:
        cursor.execute("""INSERT INTO outcomes (gametime, gamedate, player, opponent, win_or_lose, win_score, lose_score, elo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (gametime, gamedate, player, opponent, win_or_lose, win_score, lose_score, elo))
            
    print("Match registrerad")


def update_player(conn, player, win_or_lose, elo):
    with conn.cursor() as cursor:

        if win_or_lose == "win":
            cursor.execute("""UPDATE players \
                    SET matches = matches + 1, wins = wins + 1, elo = %s \
                    WHERE player = %s""", (elo, player))
        else:
            cursor.execute("""UPDATE players \
                            SET matches = matches + 1, losses = losses + 1, elo = %s \
                            WHERE player = %s""", (elo, player))

    print("Spelare", player, "uppdaterad")


#%%
conn = util.get_db_conn()
st.title("Registrera match")

players = util.get_player_table(conn)
win_score, lose_score = None, None

with st.form("registrera_match", clear_on_submit=True):

    left_column, right_column = st.columns(2)
    with left_column:
        winner = st.selectbox('_Vinnare_', players['name'])
        st.text_input("_Vinnarens poäng_", key="win_score", value='')
        win_score = st.session_state.win_score

    with right_column:
        loser = st.selectbox('_Förlorare_', players['name'])
        st.text_input("_Förlorarens poäng_", key="lose_score", value='')
        lose_score = st.session_state.lose_score

    # if (win_score != ''):
    #     st.error("Vinnaren måste ha en poäng")
    # if (lose_score != ''):
    #     st.error("Förloraren måste ha en poäng")
    # if int(win_score) == int(lose_score):
    #     st.error("Någon måste vinna!")
    # if winner == loser:
    #     st.error("Du kan inte spela mot dig själv!")

    submitted = st.form_submit_button("Registrera denna match")
    if submitted:

        print(win_score, lose_score, type(win_score))

        if winner == loser:
            st.error("Du kan inte spela mot dig själv!")
        elif (win_score == ''):
            st.error("Vinnaren måste ha poäng!")
        elif (lose_score == ''):
            st.error("Förloraren måste ha poäng!")
        elif int(win_score) == int(lose_score):
            st.error("Någon måste vinna!")
        elif int(win_score) < int(lose_score):
            st.error("Vinnaren måste ha mest poäng!")

        else:
            win_score = int(win_score)
            lose_score = int(lose_score)

            winner_elo = util.compute_elo(players, winner, loser, win_score, lose_score)
            loser_elo = util.compute_elo(players, loser, winner, lose_score, win_score)

            gametime = str(datetime.now())[0:-3]
            register_game(conn, gametime, winner, loser, 'winner', win_score, lose_score, winner_elo)
            register_game(conn, gametime, loser, winner, 'loser', win_score, lose_score, loser_elo)

            update_player(conn, winner, "win", winner_elo)
            update_player(conn, loser, "loose", loser_elo)

            st.success("Match registrerad")
            st.write("Vinnare:", winner,", Poäng:", win_score, ", Förlorare:", loser, "Poäng:", lose_score)

conn.close()

