from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Player, Stat, Game
from ..extensions import db
from flask_login import login_required, current_user


players_bp = Blueprint('players', __name__, url_prefix='/players')


@players_bp.route('/player_stats')
@login_required
def player_stats():
    players = Player.query.filter_by(user_id=current_user.id).all()
    player_data = []

    for player in players:
        stats = Stat.query.filter_by(player_id=player.id).all()

        player.total_points = sum(s.points for s in stats)
        player.total_assists = sum(s.assists for s in stats)
        player.total_rebounds = sum(s.total_rebounds for s in stats)
        player.total_blocks = sum(s.blocks for s in stats)
        player.total_steals = sum(s.steals for s in stats)
        player.total_fouls = sum(s.total_fouls for s in stats)
        player.total_turnovers = sum(s.total_turnovers for s in stats)
        player.minutes_played = sum(s.minutes_played for s in stats)

        player.two_pointers = sum(s.two_pointers for s in stats)
        player.three_pointers = sum(s.three_pointers for s in stats)
        player.free_throws = sum(s.free_throws for s in stats)

        # ✅ Add these sums:
        player.converted_assists = sum(s.converted_assists for s in stats)
        player.missed_assists = sum(s.missed_assists for s in stats)
        player.off_rebounds = sum(s.off_rebounds for s in stats)
        player.def_rebounds = sum(s.def_rebounds for s in stats)
        player.three_sec_viol = sum(s.three_sec_violations for s in stats)
        player.five_sec_viol = sum(s.five_sec_violations for s in stats)
        player.bad_passes = sum(s.bad_passes for s in stats)
        player.traveling = sum(s.traveling for s in stats)
        player.personal_fouls = sum(s.personal_fouls for s in stats)
        player.unsportsmanlike_fouls = sum(s.unsportsmanlike_fouls for s in stats)
        player.rating = sum(s.rating for s in stats)  # You can also compute avg if needed

        player_data.append(player)

    return render_template('player_stats.html', players=player_data)




@players_bp.route('/player/<int:player_id>')
@login_required
def player_detail(player_id):
    player = Player.query.filter_by(id=player_id, user_id=current_user.id).first_or_404()

    stats = Stat.query.filter_by(player_id=player.id).join(Game).order_by(Game.date.desc()).all()
    return render_template('player_detail.html', player=player, stats=stats)

@players_bp.route('/player/<int:player_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_player(player_id):
    player = Player.query.filter_by(id=player_id, user_id=current_user.id).first_or_404()


    if request.method == 'POST':
        player.name = request.form['name']
        player.position = request.form['position']
        player.jersey_number = request.form['jersey_number']
        db.session.commit()
        flash('Player updated successfully!', 'success')
        return redirect(url_for('players.player_stats'))

    return render_template('edit_player.html', player=player)

@players_bp.route('/player/<int:player_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_player(player_id):
    player = Player.query.filter_by(id=player_id, user_id=current_user.id).first_or_404()
    db.session.delete(player)
    db.session.commit()
    flash(f'Player \"{player.name}\" has been deleted.', 'danger')
    return redirect(url_for('players.player_stats'))

@players_bp.route('/add_player', methods=['GET', 'POST'])
@login_required
def add_player():
    if request.method == 'POST':
        name = request.form['name']
        jersey_number = request.form.get('jersey_number')
        position = request.form.get('position')
        jersey_number = int(jersey_number) if jersey_number else None

        new_player = Player(
            name=name,
            jersey_number=jersey_number,
            position=position,
            team_id=current_user.team_id,
            user_id=current_user.id  # ✅ Critical!
        )

        db.session.add(new_player)
        db.session.commit()
        flash('Player added successfully!', 'success')
        return redirect(url_for('players.player_stats'))

    return render_template("add_player.html")

@players_bp.route('/add_stat', methods=['GET', 'POST'])
@login_required
def add_stat():
    players = Player.query.filter_by(team_id=current_user.team_id, user_id=current_user.id).all()
    games = Game.query.filter_by(team_id=current_user.team_id).all()

    if request.method == 'POST':
        player_id = int(request.form.get('player_id'))
        game_id = int(request.form.get('game_id'))

        two_pointers = int(request.form.get('two_pointers') or 0)
        three_pointers = int(request.form.get('three_pointers') or 0)
        free_throws = int(request.form.get('free_throws') or 0)

        off_rebounds = int(request.form.get('off_rebounds') or 0)
        def_rebounds = int(request.form.get('def_rebounds') or 0)

        assists = int(request.form.get('assists') or 0)
        converted_assists = int(request.form.get('converted_assists') or 0)
        missed_assists = int(request.form.get('missed_assists') or 0)

        blocks = int(request.form.get('blocks') or 0)
        steals = int(request.form.get('steals') or 0)

        personal_fouls = int(request.form.get('personal_fouls') or 0)
        unsportsmanlike_fouls = int(request.form.get('unsportsmanlike_fouls') or 0)

        turnovers = int(request.form.get('turnovers') or 0)
        three_sec_violations = int(request.form.get('three_sec_violations') or 0)
        five_sec_violations = int(request.form.get('five_sec_violations') or 0)
        bad_passes = int(request.form.get('bad_passes') or 0)
        traveling = int(request.form.get('traveling') or 0)

        minutes_played = int(request.form.get('minutes_played') or 0)

        stat = Stat(
            player_id=player_id,
            game_id=game_id,
            two_pointers=two_pointers,
            three_pointers=three_pointers,
            free_throws=free_throws,
            assists=assists,
            converted_assists=converted_assists,
            missed_assists=missed_assists,
            off_rebounds=off_rebounds,
            def_rebounds=def_rebounds,
            blocks=blocks,
            steals=steals,
            personal_fouls=personal_fouls,
            unsportsmanlike_fouls=unsportsmanlike_fouls,
            turnovers=turnovers,
            three_sec_violations=three_sec_violations,
            five_sec_violations=five_sec_violations,
            bad_passes=bad_passes,
            traveling=traveling,
            minutes_played=minutes_played
        )

        db.session.add(stat)
        db.session.commit()
        flash("Stat added successfully", "success")
        return redirect(url_for('dashboard.dashboard'))

    return render_template('add_stat.html', players=players, games=games)


@players_bp.route('/add_stats/<int:game_id>', methods=['GET', 'POST'])
@login_required
def add_stats(game_id):
    game = Game.query.get_or_404(game_id)
    players = Player.query.filter_by(team_id=current_user.team_id, user_id=current_user.id).all()


    if request.method == 'POST':
        for player in players:
            stat = Stat(
                game_id=game.id,
                player_id=player.id,
                points=int(request.form.get(f'points_{player.id}', 0)),
                assists=int(request.form.get(f'assists_{player.id}', 0)),
                rebounds=int(request.form.get(f'rebounds_{player.id}', 0)),
                steals=int(request.form.get(f'steals_{player.id}', 0)),
                blocks=int(request.form.get(f'blocks_{player.id}', 0)),
                fouls=int(request.form.get(f'fouls_{player.id}', 0)),
                turnovers=int(request.form.get(f'turnovers_{player.id}', 0)),
                minutes_played=int(request.form.get(f'minutes_{player.id}', 0)),
            )
            db.session.add(stat)
        db.session.commit()
        return redirect(url_for('games.games'))

    return render_template('add_stats.html', game=game, players=players)
