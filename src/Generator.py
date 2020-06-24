import Parser
import numpy as np
from sklearn import preprocessing


def generate(paths):
    games = Parser.parse(paths)
    X = []
    y = []
    for game in games:
        vector = []
        #vector.append(game.result)                      # should be 100%

        last_three_games_home_team = last_three_games(game.home_team, game.date, games)
        season_games_home_team = season_games(game.home_team, game.date, games)
        last_game_home_team = last_game(game.home_team, game.date, games)
        weekly_rest_home_team = weekly_rest(game.home_team, game.date, games)
        yesterday_rest_home_team = yesterday_rest(game.home_team, game.date, games)
        last_three_games_away_team = last_three_games(game.away_team, game.date, games)
        season_games_away_team = season_games(game.away_team, game.date, games)
        last_game_away_team = last_game(game.away_team, game.date, games)
        weekly_rest_away_team = weekly_rest(game.away_team, game.date, games)
        yesterday_rest_away_team = yesterday_rest(game.away_team, game.date, games)

        if len(last_three_games_home_team) < 3 or len(last_three_games_away_team) < 3:
            continue

        #vector += average(last_three_games_home_team)  # not
        vector += average(season_games_home_team)
        #vector += last_game_home_team.vector           # not
        vector.append(weekly_rest_home_team)
        vector.append(yesterday_rest_home_team)
        #vector += average(last_three_games_away_team)  # not
        vector += average(season_games_away_team)
        #vector += last_game_away_team.vector           # not
        #vector.append(weekly_rest_away_team)           # not
        vector.append(yesterday_rest_away_team)

        X.append(vector)
        y.append(game.result)

    X = preprocessing.scale(np.asarray(X))
    X = preprocessing.normalize(np.asarray(X), norm='l2')
    return X, y


def average(games):
    vector = []
    n = len(games)
    for i in range(len(games[0].vector)):
        total = 0.0
        for game in games:
            total += game.vector[i]
        vector.append(total/n)
    return vector


def same_date(date1, date2):
    if date1[0] == date2[0] and date1[1] == date2[1] and date1[2] == date2[2]:
        return True
    return False


def before(date1, date2):
    if date1[2] > date2[2]:  # Year
        return False
    elif date1[2] < date2[2]:
        return True
    if date1[0] > date2[0]:  # Month
        return False
    elif date1[0] < date2[0]:
        return True
    if date1[1] > date2[1]:  # Day
        return False
    else:
        return True


# Merge sort
def sort(games):
    if len(games) > 1:
        mid = len(games) // 2
        left_half = games[:mid]
        right_half = games[mid:]

        sort(left_half)
        sort(right_half)

        i = 0
        j = 0
        k = 0
        while i < len(left_half) and j < len(right_half):
            if before(left_half[i].date, right_half[j].date):
                games[k] = left_half[i]
                i = i + 1
            else:
                games[k] = right_half[j]
                j = j + 1
            k = k + 1

        while i < len(left_half):
            games[k] = left_half[i]
            i = i + 1
            k = k + 1

        while j < len(right_half):
            games[k] = right_half[j]
            j = j + 1
            k = k + 1
    return games


# Can return empty list
def last_three_games(team, date, games):
    last_three_games = []
    for game in games:
        if not same_date(game.date, date):
            if game.home_team == team or game.away_team == team:
                if before(game.date, date):
                    if len(last_three_games) < 3:
                        last_three_games.append(game)
                        last_three_games = sort(last_three_games)
                    else:
                        if before(last_three_games[0].date, game.date):
                            last_three_games.remove(last_three_games[0])
                            last_three_games.append(game)
                            last_three_games = sort(last_three_games)

    return last_three_games


# Can return empty list
def season_games(team, date, games):
    season_games = []
    for game in games:
        if not same_date(game.date, date):
            if game.home_team == team or game.away_team == team:
                if before(game.date, date):
                    season_games.append(game)
    return season_games


# Can return None
def last_game(team, date, games):
    last_game = None
    for game in games:
        if not same_date(game.date, date):
            if game.home_team == team or game.away_team == team:
                if before(game.date, date):
                    if last_game is None or before(last_game.date, game.date):
                        last_game = game
    return last_game


def weekly_rest(team, date, games):
    rest = 7.0
    for game in games:
        if game.home_team == team or game.away_team == team:
            if not same_date(date, game.date):
                if date[0] == game.date[0] and date[2] == game.date[2]:  # Same year and month
                    if game.date[1] >= date[1] - 7:
                        rest -= 1
    return rest


def yesterday_rest(team, date, games):
    for game in games:
        if game.home_team == team or game.away_team == team:
            if date[0] == game.date[0] and date[2] == game.date[2]:  # Same year and month
                if game.date[1] == (date[1] - 1):
                    return 1.0
    return 0.0
