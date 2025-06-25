from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Game, Team, Stat, Player
from ..extensions import db
from datetime import datetime

# ✅ Define blueprint at the top
games_bp = Blueprint('games', __name__, url_prefix='/games')


# 🏀 View list of games
@games_bp.route('/')
@login_required
def games():
    games = Game.query.filter_by(team_id=current_user.team_id).order_by(Game.date.desc()).all()
    return render_template("games.html", games=games)


# 🏀 View a single game
@games_bp.route('/<int:game_id>')
@login_required
def view_game(game_id):
    game = Game.query.get_or_404(game_id)
    return render_template('view_game.html', game=game)


# 🏀 Add a new game
@games_bp.route('/add_game', methods=['GET', 'POST'])
@login_required
def add_game():
    if request.method == 'POST':
        date_str = request.form['date']
        date = datetime.strptime(date_str, "%Y-%m-%d").date()

        opponent = request.form['opponent']
        location = request.form['location']
        result = request.form['result']
        team_score = int(request.form['team_score'])
        opponent_score = int(request.form['opponent_score'])

        # ✅ Automatically assign current user's team
        team_id = current_user.team_id

        new_game = Game(
            date=date,
            opponent=opponent,
            location=location,
            result=result,
            team_score=team_score,
            opponent_score=opponent_score,
            team_id=team_id
        )
        db.session.add(new_game)
        db.session.commit()
        flash('Game added successfully!', 'success')
        return redirect(url_for('games.games'))

    return render_template("add_game.html")


# 🏀 Edit game
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
        flash('Game updated successfully.', 'success')
        return redirect(url_for('games.view_game', game_id=game.id))

    return render_template('edit_game.html', game=game)


# 🏀 Delete game
@games_bp.route('/<int:game_id>/delete', methods=['POST'])
@login_required
def delete_game(game_id):
    game = Game.query.get_or_404(game_id)

    # Also delete associated stats
    Stat.query.filter_by(game_id=game.id).delete()
    db.session.delete(game)
    db.session.commit()
    flash('Game deleted successfully.', 'success')

    return redirect(url_for('games.games'))
