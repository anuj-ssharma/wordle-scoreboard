import json

from app import app
from flask import render_template
from flask import request, redirect, url_for

from app.leaderboard import Leaderboard
from app.playerresults import PlayerResults
from datetime import date


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html', today=196 + (date.today() - date(2022, 1, 1)).days)


@app.route('/submit_results', methods=['POST'])
def submit_results():
    user_results = request.form['results']
    player_result = PlayerResults(request.form['player_name'])
    if player_result.parse(user_results) and player_result.save_result():
        return redirect(url_for('leaderboard'))
    return redirect(url_for('failure'))


@app.route('/save')
def success():
    return render_template('index.html',  msg='Results saved successfully.')


@app.route('/failure')
def failure():
    return render_template('index.html',  msg='Sorry but we could not save your results.')


@app.route('/leaderboard')
def leaderboard():
    leaderboard_results = Leaderboard().today_leaderboard()
    return render_template('leaderboard.html',
                           today=196 + (date.today() - date(2022, 1, 1)).days,
                           leaderboard=leaderboard_results)


@app.route('/alltime')
def alltime_leaderboard():
    alltime_leaderboard_results = Leaderboard().all_time_leaderboard()
    return json.dumps(alltime_leaderboard_results)