from flask import Flask, render_template, redirect, url_for, request, session, flash
from extensions import db
from models import User, Player, Team, Game, Stat
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import func
from datetime import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv
import os

# Initialize Flask app and database


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///basketball.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


serializer = URLSafeTimedSerializer(app.secret_key)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




# --------------- Core Routes ---------------
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route("/dashboard")
def dashboard():
    total_players = Player.query.count()
    total_games = Game.query.count()
    total_points = db.session.query(db.func.sum(Stat.points)).scalar() or 0

    recent_games = Game.query.order_by(Game.date.desc()).limit(5).all()

    # Data for chart
    chart_labels = [game.date.strftime('%b %d') for game in recent_games[::-1]]
    chart_scores = [game.team_score for game in recent_games[::-1]]

    return render_template(
        "dashboard.html",
        total_players=total_players,
        total_games=total_games,
        total_points=total_points,
        recent_games=recent_games,
        chart_labels=chart_labels,
        chart_scores=chart_scores
    )

# --------------- Authentication Routes ---------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash("Invalid credentials")
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if user:
            token = user.get_reset_token(app.secret_key)
            reset_url = url_for('reset_password', token=token, _external=True)
            flash(f'Password reset link (simulate): {reset_url}', 'info')
        else:
            flash('No account found with that username.', 'danger')
    return render_template('forgot_password.html')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_token(token, app.secret_key)
    if not user:
        flash('Invalid or expired token.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_password = request.form.get('password')
        user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html')


    if request.method == 'POST':
        new_password = request.form.get('password')
        user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html')


# --------------- Player Routes ---------------

@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        name = request.form['name']
        jersey_number = request.form.get('jersey_number')
        position = request.form.get('position')
        jersey_number = int(jersey_number) if jersey_number else None

        new_player = Player(
            name=name,
            jersey_number=jersey_number,
            position=position
        )
        db.session.add(new_player)
        db.session.commit()
        return redirect(url_for('home'))
    
    return render_template("add_player.html")

@app.route('/player_stats')
def player_stats():
    players = Player.query.all()
    player_data = []

    for player in players:
        stats = Stat.query.filter_by(player_id=player.id).all()
        total_points = sum(s.points for s in stats)
        total_assists = sum(s.assists for s in stats)
        total_rebounds = sum(s.rebounds for s in stats)

        player.total_points = total_points
        player.total_assists = total_assists
        player.total_rebounds = total_rebounds

        player_data.append(player)

    return render_template('player_stats.html', players=player_data)


@app.route('/player/<int:player_id>')
def player_detail(player_id):
    player = Player.query.get_or_404(player_id)
    stats = Stat.query.filter_by(player_id=player.id).join(Game).order_by(Game.date.desc()).all()
    return render_template('player_detail.html', player=player, stats=stats)


@app.route('/player/<int:player_id>/edit', methods=['GET', 'POST'])
def edit_player(player_id):
    player = Player.query.get_or_404(player_id)

    if request.method == 'POST':
        player.name = request.form['name']
        player.position = request.form['position']
        player.jersey_number = request.form['jersey_number']
        db.session.commit()
        flash('Player updated successfully!', 'success')
        return redirect(url_for('player_stats'))

    return render_template('edit_player.html', player=player)


@app.route('/player/<int:player_id>/delete', methods=['POST', 'GET'])
def delete_player(player_id):
    player = Player.query.get_or_404(player_id)
    db.session.delete(player)
    db.session.commit()
    flash(f'Player "{player.name}" has been deleted.', 'danger')
    return redirect(url_for('player_stats'))

@app.route('/add_stat', methods=['GET', 'POST'])
def add_stat():
    players = Player.query.all()
    games = Game.query.all()

    if request.method == 'POST':
        player_id = request.form.get('player_id')
        game_id = request.form.get('game_id')
        points = request.form.get('points')
        rebounds = request.form.get('rebounds')
        assists = request.form.get('assists')
        blocks = request.form.get('blocks')
        steals = request.form.get('steals')

        stat = Stat(
            player_id=player_id,
            game_id=game_id,
            points=points,
            rebounds=rebounds,
            assists=assists,
            blocks=blocks,
            steals=steals
        )
        db.session.add(stat)
        db.session.commit()
        flash("Stat added successfully", "success")
        return redirect(url_for('dashboard'))

    return render_template('add_stat.html', players=players, games=games)

@app.route('/add_stats/<int:game_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('games'))

    return render_template('add_stats.html', game=game, players=players)



# --------------- Team Routes ---------------


@app.route('/team_stats')
def team_stats():
    total_stats = db.session.query(
        func.sum(Stat.points),
        func.sum(Stat.assists),
        func.sum(Stat.rebounds),
        func.sum(Stat.steals),
        func.sum(Stat.blocks),
        func.sum(Stat.turnovers)
    ).first()

    total_games = Game.query.count() or 1  # Avoid division by zero

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

    return render_template('team_stats.html', totals=totals, averages=averages)


@app.route('/team_profile')
def team_profile():
    team = Team.query.first()
    return render_template('team_profile.html', team=team)

@app.route('/add_team', methods=['GET', 'POST'])
def add_team():
    if request.method == 'POST':
        name = request.form['name']
        coach_name = request.form.get('coach_name')

        new_team = Team(
            name=name,
            coach_name=coach_name
        )
        db.session.add(new_team)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add_team.html")

# --------------- Game Routes ---------------

@app.route('/games')
def games():
    games = Game.query.all()
    return render_template("games.html", games=games)

@app.route('/game/<int:game_id>')
def view_game(game_id):
    game = Game.query.get_or_404(game_id)
    return render_template('view_game.html', game=game)

@app.route('/add_game', methods=['GET', 'POST'])
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
            team_id=team_id
        )
        db.session.add(new_game)
        db.session.commit()
        return redirect(url_for('games'))  # or wherever you want

    return render_template("add_game.html", teams=teams)


@app.route('/edit_game/<int:game_id>', methods=['GET', 'POST'])
def edit_game(game_id):
    game = Game.query.get_or_404(game_id)

    if request.method == 'POST':
        # Convert date string to a Python date object
        date_str = request.form['date']  # 'YYYY-MM-DD'
        game.date = datetime.strptime(date_str, '%Y-%m-%d').date()

        game.opponent = request.form['opponent']
        game.location = request.form['location']
        game.result = request.form['result']
        game.team_score = int(request.form['team_score'])
        game.opponent_score = int(request.form['opponent_score'])

        db.session.commit()
        return redirect(url_for('games'))

    return render_template('edit_game.html', game=game)



@app.route('/games/<int:game_id>/delete', methods=['POST'])
def delete_game(game_id):
    game = Game.query.get_or_404(game_id)

    # Also delete any stats associated with the game
    Stat.query.filter_by(game_id=game.id).delete()

    db.session.delete(game)
    db.session.commit()
    
    flash('Game deleted successfully.', 'success')
    return redirect(url_for('games'))  # or wherever you list games




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
