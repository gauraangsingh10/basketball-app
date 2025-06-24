from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Team, Stat, Game, Player
from ..extensions import db
from flask_login import login_required, current_user

teams_bp = Blueprint('teams', __name__, url_prefix='/teams')


@teams_bp.route('/team_stats')
@login_required
def team_stats():
    team = current_user.team

    if not team:
        return render_template(
            'team_stats.html',
            team=None,
            totals={},
            averages={}
        )

    total_stats = db.session.query(
        db.func.sum(Stat.points),
        db.func.sum(Stat.assists),
        db.func.sum(Stat.rebounds),
        db.func.sum(Stat.steals),
        db.func.sum(Stat.blocks),
        db.func.sum(Stat.turnovers)
    ).join(Player).filter(Player.team_id == team.id).first()

    total_games = Game.query.filter_by(team_id=team.id).count() or 1

    totals = {
        'points': total_stats[0] or 0,
        'assists': total_stats[1] or 0,
        'rebounds': total_stats[2] or 0,
        'steals': total_stats[3] or 0,
        'blocks': total_stats[4] or 0,
        'turnovers': total_stats[5] or 0,
        'games': total_games
    }

    averages = {
        'points': round(totals['points'] / total_games, 1),
        'assists': round(totals['assists'] / total_games, 1),
        'rebounds': round(totals['rebounds'] / total_games, 1),
        'steals': round(totals['steals'] / total_games, 1),
        'blocks': round(totals['blocks'] / total_games, 1),
        'turnovers': round(totals['turnovers'] / total_games, 1),
    }

    return render_template('team_stats.html', team=team, totals=totals, averages=averages)


@teams_bp.route('/team_profile')
@login_required
def team_profile():
    team = Team.query.first()
    return render_template('team_profile.html', team=team)


@teams_bp.route('/add_team', methods=['GET', 'POST'])
@login_required
def add_team():
    if request.method == 'POST':
        name = request.form['name']
        coach_name = request.form.get('coach_name')

        new_team = Team(name=name, coach_name=coach_name)
        db.session.add(new_team)
        db.session.commit()

        # ✅ Assign the team to current user
        current_user.team_id = new_team.id
        db.session.commit()

        flash("Team created and assigned!", "success")
        return redirect(url_for('dashboard.dashboard'))

    return render_template("add_team.html")

@teams_bp.route('/team/<int:team_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)

    # Optional: Prevent deleting if the team has players or games
    if team.players or team.games:
        flash("Cannot delete team with players or games. Please delete them first.", "danger")
        return redirect(url_for('teams.team_stats'))

    db.session.delete(team)
    db.session.commit()
    flash(f'Team "{team.name}" has been deleted.', 'success')
    return redirect(url_for('teams.team_stats'))

