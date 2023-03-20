DROP TABLE players;
CREATE TABLE players (
    player varchar(40),
    matches int,
    wins int,
    losses int,
    elo float
);

DROP TABLE outcomes;
CREATE TABLE outcomes (
    gametime datetime2,
    gamedate date,
    player varchar(40),
    opponent varchar(40),
    win_or_lose varchar(10),
    win_score int,
    lose_score int,
    elo float,
);

DROP TABLE matches;
CREATE TABLE matches (
    gametime datetime2,
    winner varchar(40),
    loser varchar(40),
    win_score int,
    lose_score int,
);
