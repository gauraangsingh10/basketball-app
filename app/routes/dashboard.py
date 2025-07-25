from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models import Player, Game, Stat
from ..extensions import db
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    team_id = current_user.team_id

    total_players = Player.query.filter_by(team_id=team_id, user_id=current_user.id).count()
    total_games = Game.query.filter_by(team_id=team_id).count()

    # Sum points directly via two_pointers, three_pointers, free_throws
    total_points = (
        db.session.query(
            func.sum(Stat.two_pointers * 2 + Stat.three_pointers * 3 + Stat.free_throws)
        )
        .join(Player, Stat.player_id == Player.id)
        .filter(Player.team_id == team_id, Player.user_id == current_user.id)
        .scalar() or 0
    )

    recent_games = (
        Game.query.filter_by(team_id=team_id)
        .order_by(Game.date.desc())
        .limit(5)
        .all()
    )

    chart_labels = [game.date.strftime('%b %d') for game in reversed(recent_games)]
    chart_scores = [game.team_score for game in reversed(recent_games)]

    return render_template(
        'dashboard.html',
        total_players=total_players,
        total_games=total_games,
        total_points=total_points,
        recent_games=recent_games,
        chart_labels=chart_labels,
        chart_scores=chart_scores
    )
