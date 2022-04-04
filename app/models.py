from app import db


class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wordle_number = db.Column(db.String, nullable=False)
    player_name = db.Column(db.String(50), nullable=False)
    solved = db.Column(db.Boolean, nullable=True)
    guesses = db.Column(db.Integer, nullable=False)
    grid = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return '<Result {}>'.format(self.player_name)
