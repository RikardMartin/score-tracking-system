INSERT INTO
    players (player, matches, wins, losses, elo)
VALUES
    ('Anna Andersson', 3, 2, 1, 2),
    ('Richard Richardsson', 6, 1, 6, -0.5),
    ('Emma Emmasson', 5, 4, 1, 7.5);

SELECT * from players;


INSERT INTO matches
    (gametime, winner, loser, win_score, lose_score)
VALUES
    ('2022-11-05 12:01:02', 'Anna Andersson', 'Richard Richardsson', 11, 0),
    ('2022-11-05 12:15:02', 'Anna Andersson', 'Richard Richardsson', 11, 5),
    ('2022-11-05 12:30:02', 'Emma Emmasson', 'Anna Andersson', 5, 6),
    ('2022-11-06 00:01:02', 'Richard Richardsson', 'Emma Emmasson', 11, 8),
    ('2022-11-06 00:15:03', 'Emma Emmasson', 'Richard Richardsson', 11, 8),
    ('2022-11-08 00:00:00', 'Emma Emmasson', 'Richard Richardsson', 21, 20),
    ('2022-11-08 00:01:01', 'Emma Emmasson', 'Richard Richardsson', 11, 6);

SELECT * from matches;


INSERT INTO outcomes
    (gametime, gamedate, elo, win_or_lose, player)
VALUES
    ('2022-11-05 12:01:02', '2022-11-05', 3, 'winner', 'Anna Andersson'),
    ('2022-11-05 12:15:02', '2022-11-05', 2, 'winner', 'Anna Andersson'),
    ('2022-11-05 12:30:02', '2022-11-05', 1, 'winner', 'Emma Emmasson'),
    ('2022-11-06 00:01:02', '2022-11-06', 0, 'winner', 'Richard Richardsson'),
    ('2022-11-06 00:15:03', '2022-11-06', -1, 'winner', 'Emma Emmasson'),
    ('2022-11-08 00:00:00', '2022-11-08', -2, 'winner', 'Emma Emmasson'),
    ('2022-11-08 00:01:01', '2022-11-08', -3, 'winner', 'Emma Emmasson'),

    ('2022-11-05 12:01:02', '2022-11-05', 15.5, 'loser', 'Richard Richardsson'),
    ('2022-11-05 12:15:02', '2022-11-05', 12.5, 'loser', 'Richard Richardsson'),
    ('2022-11-05 12:30:02', '2022-11-05', 14.5, 'loser', 'Anna Andersson'),
    ('2022-11-06 00:01:02', '2022-11-06', -5, 'loser', 'Emma Emmasson'),
    ('2022-11-06 00:15:03', '2022-11-06', -5, 'loser', 'Richard Richardsson'),
    ('2022-11-08 00:00:00', '2022-11-08', -0.5, 'loser', 'Richard Richardsson'),
    ('2022-11-08 00:01:01', '2022-11-08', -1, 'loser', 'Richard Richardsson');

SELECT * from outcomes;
