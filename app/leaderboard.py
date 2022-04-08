import json

from app.models import Results
from app import db
from datetime import date


class Leaderboard:
    def __init__(self):
        self.today = 196 + (date.today() - date(2022, 1, 1)).days

    def today_leaderboard(self):
        today = 196 + (date.today() - date(2022, 1, 1)).days
        today_results_solved = db.session.query(Results).filter(Results.wordle_number == str(today),
                                                                Results.solved == True)
        today_results_unsolved = db.session.query(Results).filter(Results.wordle_number == str(today),
                                                                  Results.solved == False)
        today_leaderboard_results = today_results_solved.order_by(Results.guesses)

        leaderboard = []

        for player in today_leaderboard_results.all():
            formatted_grid = []
            for row in json.loads(player.grid):
                row = row.replace('🟩', str(2))
                row = row.replace('⬛', str(0))
                row = row.replace('🟨', str(1))
                formatted_grid.append(row)
            leaderboard.append({'name': player.player_name, 'guesses': player.guesses, 'grid': formatted_grid})

        for player in today_results_unsolved.all():
            leaderboard.append({'name': player.player_name, 'guesses': player.guesses, 'grid': formatted_grid})

        return leaderboard

    def all_time_leaderboard(self):
        players = ['Anuj', 'Nikhil', 'Soumya', 'Rachana']
        alltime_leaderboard = {}
        for player in players:
            results = db.session.query(Results).filter_by(player_name=player)
            total_solved = 0
            total_unsolved = 0
            total_results = results.count()
            score = 0
            for result in results:
                if result.guesses != 0:
                    score += result.guesses
                    total_solved += 1
            avg_score = float("{:.2f}".format(score / total_solved))
            total_unsolved = total_results - total_solved
            alltime_leaderboard.update({player: {}})
            player_result = {"score": avg_score,
                             "total_played": total_results,
                             "total_solved": total_solved,
                             "total_unsolved": total_unsolved}
            alltime_leaderboard.update({player: player_result})

        return alltime_leaderboard
        # return flask.jsonify(alltime_leaderboard)
        # return {k: v for k, v in sorted(alltime_leaderboard.items(), key=lambda item: item[1])}
