import pandas as pd
import os
import streamlit as st
import pymssql

#%% PARAMETERS

START_ELO = 100


# På Azure deployment
db_name = os.getenv('AZURE_SQL_DATABASE')
db_password = os.getenv('AZURE_SQL_PASSWORD')
db_port = os.getenv('AZURE_SQL_PORT')
db_server = os.getenv('AZURE_SQL_SERVER')
db_user = os.getenv('AZURE_SQL_USER')
db_driver = '{ODBC Driver 18 for SQL Server}'

# För lokal utveckling
db_name = 'pingis_db'
db_password = '###'
db_port = '1433'
db_server = 'gbgpingis.database.windows.net'
db_user = '###'
db_driver = '{ODBC Driver 18 for SQL Server}'


def get_db_conn():
    # conn = pyodbc.connect('DRIVER='+db_driver+';SERVER=tcp:'+db_server+';PORT='+db_port+';DATABASE='+db_name+';UID='+db_user+';PWD='+ db_password)
    conn = pymssql.connect(server=db_server, user=db_user, password=db_password, database=db_name, port=db_port, autocommit=True)
    return conn

def get_player_table(conn):
    rows = []
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM players WHERE CHARINDEX('Testperson', player) = 0;")
        rows = cursor.fetchall()

    rows = [tuple(entry) for entry in rows]
    df = pd.DataFrame(rows, columns=["name", "matches", "wins", "losses", "elo"])


    return df


def get_outcomes_table(conn):
    rows = []

    with conn.cursor() as cursor:
        cursor.execute("SELECT * from outcomes")
        rows = cursor.fetchall()

    rows = [tuple(entry) for entry in rows]
    df = pd.DataFrame(rows, columns=["gametime", "gamedate", "player", "opponent", "win_or_lose", "win_score", "lose_score", "elo"])
    return df


def compute_elo(players, player, opponent, my_score, op_score):
    old_elo = players[players['name'] == player]['elo'].values[0]
    old_op_elo = players[players['name'] == opponent]['elo'].values[0]


    # Chess elo with a custom score normalization
    E_player = 1/(1 + 10**((old_op_elo - old_elo)/400))
    # weighted_score = 1 if my_score > op_score else 0
    weighted_score = ( 1 + (my_score - op_score)/max([my_score, op_score]) ) / 2
    elo = old_elo + 24*(weighted_score - E_player)
    
    
    # Custom balanced rating
    # elo = old_elo + 16*(my_score - op_score) * (old_op_elo / old_elo)

    print(f"player={player}, opponent={opponent}, my_score={my_score}, op_score={op_score}, my_elo={old_elo}, op_elo={old_op_elo}")
       
    return elo

#%%
if __name__ == "__main__":
    conn = get_db_conn()

    st.title("GBG Pingis")
    
    st.markdown("## Poängtavla")
    st.markdown("Visar endast spelare med minst tre spelade matcher")
    players = get_player_table(conn)
    players = players[players['matches']>=3]
    players = players[players['name']!='Välj vinnare']
    players = players[players['name']!='Välj förlorare']
    
    def highlight_row(row):
        # opacity = 'rgba(105,105,105,0.2)' if row.matches <= 3 else 'white'
        opacity = '20%' if row.matches <= 3 else '100%'
        # return [f"background: rgba('105,105,105', {opacity}"]*len(row)
        # return [f'color:{opacity}, background-color: black']*len(row)
        return [f'opacity:{opacity}']*len(row)
    # st.dataframe(players.style.apply(highlight_row, axis=1))
    players['rank'] = players['elo'].rank(method='min', ascending=False).astype(int)
    st.dataframe(players)

    st.markdown("## Matcher")
    matches = get_outcomes_table(conn)
    st.dataframe(matches.drop(columns=['gamedate', 'elo']))

    conn.close()



