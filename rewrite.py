#%%
import GBG_Pingis as util

def reset_player_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("""UPDATE players \
                    SET matches = 0, wins = 0, losses = 0, elo = %s""", util.START_ELO)


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

        print(player, "uppdaterad med", win_or_lose, ":", elo, 'elo')
        cursor.execute("""SELECT player, elo \
                        FROM players \
                        WHERE player = %s""", player)
        print(cursor.fetchall())


def update_matches(conn, game_time, winner_or_loser, elo):
    with conn.cursor() as cursor:

        cursor.execute("""UPDATE outcomes \
                SET elo = %s \
                WHERE gametime = %s \
                AND win_or_lose = %s""", (elo, game_time, winner_or_loser))

        print(game_time, winner_or_loser, "elo uppdaterad:", elo)
        cursor.execute("""SELECT elo \
                        FROM outcomes \
                        WHERE gametime = %s \
                        AND win_or_lose = %s""", (game_time, winner_or_loser))
        print("databas elo:", cursor.fetchall())



#%% REWRITE PLAYER STATS
"""
resetta playerstabellen till "startläge"
sort outcomes table by date
for entry in outcomes table:
    update winner and loser players table entries with match results
    set correct elo values in matches table

"""
conn = util.get_db_conn()
reset_player_table(conn)

players = util.get_player_table(conn)
outcomes = util.get_outcomes_table(conn)
outcomes.sort_values(by='gametime', inplace=True)
print(players)
print(outcomes)

#%%
one_row_processed = {id: False for id in outcomes['gametime']}
win_elos, lose_elos = {}, {}

for ix, row in outcomes.iterrows():

    game_time = outcomes.loc[ix, 'gametime']
    game_time_str = str(game_time)[0:-3]
    players = util.get_player_table(conn)
    win_score = row['win_score']
    lose_score = row['lose_score']

    if row['win_or_lose'] == 'winner':
        winner = row['player']
        loser = row['opponent']
        win_elo = util.compute_elo(players, winner, loser, win_score, lose_score)
        win_elos[game_time] = win_elo
        update_matches(conn, game_time, 'winner', win_elo)

    else:
        winner = row['opponent']
        loser = row['player']
        lose_elo = util.compute_elo(players, loser, winner, lose_score, win_score)
        lose_elos[game_time] = lose_elo
        update_matches(conn, game_time, 'loser', lose_elo)

    if one_row_processed[game_time]:
        update_player(conn, winner, "win", win_elos[game_time])
        update_player(conn, loser, "loose", lose_elos[game_time])
        print(game_time, "| ##################################")
        
    else: one_row_processed[game_time] = True
    print('\n')   

outcomes = util.get_outcomes_table(conn)
print(outcomes)
players = util.get_player_table(conn)
print(players)

conn.close()


# %%
