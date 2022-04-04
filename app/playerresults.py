import json

from app.models import Results
from app import db


class PlayerResults:
    def __init__(self, player_name):
        self.player_name = player_name
        self.wordle_number = None
        self.solved = False
        self.solved_in_rows = 0
        self.grid = None
        self.result_to_save = None

    def parse(self, copied_result):
        player_result = copied_result.split('\r\n')
        self.wordle_number = player_result[0].split()[1]
        wordle_score = player_result[0].split()[2]

        if is_solved(wordle_score):
            self.solved = True
            rows = player_result[2:]
            self.solved_in_rows = len(rows)
            self.grid = player_result[2:]

        if self.wordle_number is not None:
            return True
        else:
            return False

    def save_result(self):
        if self.wordle_number is not None:
            result = Results(wordle_number=self.wordle_number,
                             player_name=self.player_name,
                             solved=self.solved,
                             guesses=self.solved_in_rows,
                             grid=json.dumps(self.grid))
            if not self.already_submitted():
                db.session.add(result)
                db.session.commit()
                return True
        return False

    def already_submitted(self):
        query = db.session.query(Results).filter(Results.player_name == self.player_name,
                                                 Results.wordle_number == self.wordle_number)
        if query.count() > 0:
            return True
        else:
            return False


def is_solved(wordle_score):
    return 'x' not in wordle_score.lower()
