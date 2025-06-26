from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Game, Team, Stat, Player
from ..extensions import db
from flask_login import login_required, current_user
from datetime import datetime

games_bp = Blueprint('games', __name__, url_prefix='/games')

@games_bp.route('/')
@login_required
def games():
    games = Game.query.all()
    return render_template("games.html", games=games)

@games_bp.route('/<int:game_id>')
@login_required
def view_game(game_id):
    game = Game.query.get_or_404(game_id)
    return render_template('view_game.html', game=game)

@games_bp.route('/add_game', methods=['GET', 'POST'])
@login_required
def add_game():
    teams = Team.query.all()
    if request.method == 'POST':
        date_str = request.form['date']
        date = datetime.strptime(date_str, "%Y-%m-%d").date() 

        opponent = request.form['opponent']
        location = request.form['location']
        result = request.form['result']
        team_score = int(request.form['team_score'])
        opponent_score = int(request.form['opponent_score'])
        team_id = int(request.form['team_id'])

        new_game = Game(
            date=date,
            opponent=opponent,
            location=location,
            result=result,
            team_score=team_score,
            opponent_score=opponent_score,
            team_id=team_id,
            user_id=current_user.id 
        )

        db.session.add(new_game)
        db.session.commit()
        return redirect(url_for('games.games'))
    return render_template("add_game.html", teams=teams)

@games_bp.route('/<int:game_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_game(game_id):
    game = Game.query.get_or_404(game_id)

    if request.method == 'POST':
        date_str = request.form['date']
        game.date = datetime.strptime(date_str, '%Y-%m-%d').date()

        game.opponent = request.form['opponent']
        game.location = request.form['location']
        game.result = request.form['result']
        game.team_score = int(request.form['team_score'])
        game.opponent_score = int(request.form['opponent_score'])

        db.session.commit()
        return redirect(url_for('games.games'))

    return render_template('edit_game.html', game=game)

@games_bp.route('/<int:game_id>/delete', methods=['POST'])
@login_required
def delete_game(game_id):
    game = Game.query.get_or_404(game_id)
    Stat.query.filter_by(game_id=game.id).delete()
    db.session.delete(game)
    db.session.commit()
    flash('Game deleted successfully.', 'success')
    return redirect(url_for('games.games'))
