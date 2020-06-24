class Game:

    def __init__(self, date, home_team, away_team, result, duration, home_team_stats, away_team_stats):
        self.date = [float(x) for x in date.split('/')]
        self.home_team = code(home_team)
        self.away_team = code(away_team)
        if self.home_team == 0.0 or self.away_team == 0.0:
            print('Error: Team not found')
        self.result = result
        self.duration = float(duration)
        self.home_team_stats = average([float(x) for x in home_team_stats], self.duration)
        self.away_team_stats = average([float(x) for x in away_team_stats], self.duration)
        self.vector = self.home_team_stats + self.away_team_stats

    def print(self):
        print(self.vector)


def average(stats, n):
    averaged_stats = []
    to_average = [0, 1, 2, 4, 5, 7, 8] + list(range(10, 20))
    for i in range(len(stats)):
        if i in to_average:
            averaged_stats.append(stats[i]/n)
        else:
            averaged_stats.append(stats[i])
    return averaged_stats


def code(team):
    switcher = {
        'ATL': 1.0,
        'BOS': 2.0,
        'BKN': 3.0,
        'CHA': 4.0,
        'CHI': 5.0,
        'CLE': 6.0,
        'DAL': 7.0,
        'DEN': 8.0,
        'DET': 9.0,
        'GSW': 10.0,
        'HOU': 11.0,
        'IND': 12.0,
        'LAC': 13.0,
        'LAL': 14.0,
        'MEM': 15.0,
        'MIA': 16.0,
        'MIL': 17.0,
        'MIN': 18.0,
        'NOP': 19.0,
        'NYK': 20.0,
        'OKC': 21.0,
        'ORL': 22.0,
        'PHI': 23.0,
        'PHX': 24.0,
        'POR': 25.0,
        'SAC': 26.0,
        'SAS': 27.0,
        'TOR': 28.0,
        'UTA': 29.0,
        'WAS': 30.0,
    }
    return switcher.get(team, 0.0)
