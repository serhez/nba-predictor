import csv
from Game import Game


def parse(paths):

    games = []

    for path in paths:
        with open(path, 'r') as file:
            reader = csv.reader(file)
            rows = []
            for row in reader:
                rows.append(row)

            for row1 in rows:
                for row2 in rows:
                    if row1[1][4] == '@' and row1[2] == row2[2] and same_teams(row1[1], row2[1]):
                        home_stats = row2[5:]
                        away_stats = row1[5:]
                        if row1[3] == 'L':
                            result = 1.0  # Home team won
                        else:
                            result = 0.0  # Away team won
                        games.append(Game(row1[2], row1[1][-3:], row1[1][:3], result, row1[4], home_stats, away_stats))

    return games


def same_teams(string1, string2):
    if string1[:3] == string2[-3:] and string1[-3:] == string2[:3]:
        return True
    return False
