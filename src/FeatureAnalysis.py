import Parser
import Game
import numpy as np


class Stat:

    def __init__(self, id, variance, standard_deviation, predictive_score):
        self.id = id
        self.variance = variance
        self.standard_deviation = standard_deviation
        self.predictive_score = predictive_score


class TeamStat:

    def __init__(self, id, values):
        self.id = id
        self.values = values
        self.variance = 0
        self.standard_deviation = 0
        self.predictive_score = 0

    def analise(self):
        self.variance = np.var(self.values)
        self.standard_deviation = np.std(self.values)


class Team:

    def __init__(self, team, games):
        self.team = team
        self.games = games
        self.team_stats = []

    def construct(self):
        games_stats = []
        for game in self.games:
            if self.team == game.home_team:
                games_stats.append(Game.average([float(x) for x in game.home_team_stats], game.duration))
            elif self.team == game.away_team:
                games_stats.append(Game.average([float(x) for x in game.away_team_stats], game.duration))
        self.team_stats = Team.create_stats(games_stats)
        for team_stat in self.team_stats:
            team_stat.analise()

    @staticmethod
    def create_stats(games_stats):
        team_stats = []
        for i in range(len(games_stats[0])):
            values = []
            for game_stats in games_stats:
                values.append(game_stats[i])
            team_stats.append(TeamStat(i, values))
        return team_stats


def analise_features(path):

    games = Parser.parse(path)
    team_codes = find_all_teams(games)
    teams = []
    stats = []

    for team_code in team_codes:
        team_games = []
        for game in games:
            if team_code == game.home_team or team_code == game.away_team:
                team_games.append(game)
        team = Team(team_code, team_games)
        team.construct()
        teams.append(team)

    for i in range(len(teams[0].team_stats)):
        total_variance = 0
        total_standard_deviation = 0
        total_predictive_score = 0
        for team in teams:
            total_variance += team.team_stats[i].variance
            total_standard_deviation += team.team_stats[i].standard_deviation
            total_predictive_score += team.team_stats[i].predictive_score
        stats.append(Stat(teams[0].team_stats[i].id, total_variance/len(teams), total_standard_deviation/len(teams), total_predictive_score/len(teams)))

    for stat in stats:
        print('Stat ' + str(stat.id) + ': std = ' + str(stat.standard_deviation) + ';\tvar = ' + str(stat.variance) + ';\tpred score = ' + str(stat.predictive_score))


def find_all_teams(games):

    teams = []

    for game in games:
        team1 = game.home_team
        team2 = game.away_team
        if team1 not in teams:
            teams.append(team1)
        if team2 not in teams:
            teams.append(team2)

    return teams


path = ["../Data/2017-2018/traditional.csv"]
analise_features(path)
