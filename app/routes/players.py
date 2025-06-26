<<<<<<< HEAD
from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Player, Stat, Game
from ..extensions import db
from flask_login import login_required, current_user


players_bp = Blueprint('players', __name__, url_prefix='/players')


@players_bp.route('/player_stats')
@login_required
def player_stats():
    players = Player.query.all()
    player_data = []

    for player in players:
        stats = Stat.query.filter_by(player_id=player.id).all()
        total_points = sum(s.points for s in stats)
        total_assists = sum(s.assists for s in stats)
        total_rebounds = sum(s.rebounds for s in stats)
        total_blocks = sum(s.blocks for s in stats)
        total_steals = sum(s.steals for s in stats)
        total_fouls = sum(s.fouls for s in stats)
        total_turnovers = sum(s.turnovers for s in stats)
        minutes_played = sum(s.minutes_played for s in stats)

        # Assign values to dynamic fields
        player.total_points = total_points
        player.total_assists = total_assists
        player.total_rebounds = total_rebounds
        player.total_blocks = total_blocks
        player.total_steals = total_steals
        player.total_fouls = total_fouls
        player.total_turnovers = total_turnovers
        player.minutes_played = minutes_played

        player_data.append(player)

    return render_template('player_stats.html', players=player_data)


@players_bp.route('/player/<int:player_id>')
@login_required
def player_detail(player_id):
    player = Player.query.get_or_404(player_id)
    stats = Stat.query.filter_by(player_id=player.id).join(Game).order_by(Game.date.desc()).all()
    return render_template('player_detail.html', player=player, stats=stats)

@players_bp.route('/player/<int:player_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_player(player_id):
    player = Player.query.get_or_404(player_id)

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
    player = Player.query.get_or_404(player_id)
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
            team_id=current_user.team_id  # ✅ Important!
        )
        db.session.add(new_player)
        db.session.commit()
        flash('Player added successfully!', 'success')
        return redirect(url_for('players.player_stats'))

    return render_template("add_player.html")

@players_bp.route('/add_stat', methods=['GET', 'POST'])
@login_required
def add_stat():
    # Only fetch players and games for the current user's team
    players = Player.query.filter_by(team_id=current_user.team_id).all()
    games = Game.query.filter_by(team_id=current_user.team_id).all()

    if request.method == 'POST':
        player_id = int(request.form.get('player_id'))
        game_id = int(request.form.get('game_id'))
        points = int(request.form.get('points') or 0)
        rebounds = int(request.form.get('rebounds') or 0)
        assists = int(request.form.get('assists') or 0)
        blocks = int(request.form.get('blocks') or 0)
        steals = int(request.form.get('steals') or 0)
        fouls = int(request.form.get('fouls') or 0)
        turnovers = int(request.form.get('turnovers') or 0)
        minutes_played = int(request.form.get('minutes_played') or 0)

        stat = Stat(
            player_id=player_id,
            game_id=game_id,
            points=points,
            rebounds=rebounds,
            assists=assists,
            blocks=blocks,
            steals=steals,
            fouls=fouls,
            turnovers=turnovers,
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
    players = Player.query.filter_by(team_id=game.team_id).all()

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
=======
from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Player, Stat, Game
from ..extensions import db
from flask_login import login_required, current_user


players_bp = Blueprint('players', __name__, url_prefix='/players')


@players_bp.route('/player_stats')
@login_required
def player_stats():
    players = Player.query.all()
    player_data = []

    for player in players:
        stats = Stat.query.filter_by(player_id=player.id).all()
        total_points = sum(s.points for s in stats)
        total_assists = sum(s.assists for s in stats)
        total_rebounds = sum(s.rebounds for s in stats)
        total_blocks = sum(s.blocks for s in stats)
        total_steals = sum(s.steals for s in stats)
        total_fouls = sum(s.fouls for s in stats)
        total_turnovers = sum(s.turnovers for s in stats)
        minutes_played = sum(s.minutes_played for s in stats)

        # Assign values to dynamic fields
        player.total_points = total_points
        player.total_assists = total_assists
        player.total_rebounds = total_rebounds
        player.total_blocks = total_blocks
        player.total_steals = total_steals
        player.total_fouls = total_fouls
        player.total_turnovers = total_turnovers
        player.minutes_played = minutes_played

        player_data.append(player)

    return render_template('player_stats.html', players=player_data)


@players_bp.route('/player/<int:player_id>')
@login_required
def player_detail(player_id):
    player = Player.query.get_or_404(player_id)
    stats = Stat.query.filter_by(player_id=player.id).join(Game).order_by(Game.date.desc()).all()
    return render_template('player_detail.html', player=player, stats=stats)

@players_bp.route('/player/<int:player_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_player(player_id):
    player = Player.query.get_or_404(player_id)

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
    player = Player.query.get_or_404(player_id)
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
            team_id=current_user.team_id  # ✅ Important!
        )
        db.session.add(new_player)
        db.session.commit()
        flash('Player added successfully!', 'success')
        return redirect(url_for('players.player_stats'))

    return render_template("add_player.html")

@players_bp.route('/add_stat', methods=['GET', 'POST'])
@login_required
def add_stat():
    # Only fetch players and games for the current user's team
    players = Player.query.filter_by(team_id=current_user.team_id).all()
    games = Game.query.filter_by(team_id=current_user.team_id).all()

    if request.method == 'POST':
        player_id = int(request.form.get('player_id'))
        game_id = int(request.form.get('game_id'))
        points = int(request.form.get('points') or 0)
        rebounds = int(request.form.get('rebounds') or 0)
        assists = int(request.form.get('assists') or 0)
        blocks = int(request.form.get('blocks') or 0)
        steals = int(request.form.get('steals') or 0)
        fouls = int(request.form.get('fouls') or 0)
        turnovers = int(request.form.get('turnovers') or 0)
        minutes_played = int(request.form.get('minutes_played') or 0)

        stat = Stat(
            player_id=player_id,
            game_id=game_id,
            points=points,
            rebounds=rebounds,
            assists=assists,
            blocks=blocks,
            steals=steals,
            fouls=fouls,
            turnovers=turnovers,
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
    players = Player.query.filter_by(team_id=game.team_id).all()

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
>>>>>>> 70ff187beddc9ee504183bebd5c2abb6f07add73
