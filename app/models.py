from .extensions import db
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
        
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team = db.relationship('Team', backref='users')

    players = db.relationship('Player', backref="user", lazy=True)

    def get_reset_token(self, secret_key):
        s = URLSafeTimedSerializer(secret_key)
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, secret_key, max_age=3600):
        s = URLSafeTimedSerializer(secret_key)
        try:
            data = s.loads(token, max_age=max_age)
            return User.query.get(data['user_id'])
        except Exception:
            return None


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    coach_name = db.Column(db.String(50))
    players = db.relationship('Player', backref='team', lazy=True)
    games = db.relationship('Game', back_populates='team', lazy=True)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    jersey_number = db.Column(db.Integer, nullable=True)
    position = db.Column(db.String(20))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    stats = db.relationship('Stat', backref='player', lazy=True)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    opponent = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    result = db.Column(db.String(10))
    team_score = db.Column(db.Integer)
    opponent_score = db.Column(db.Integer)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)
    team = db.relationship('Team', back_populates='games')


class Stat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    points = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    rebounds = db.Column(db.Integer, default=0)
    steals = db.Column(db.Integer, default=0)
    blocks = db.Column(db.Integer, default=0)
    fouls = db.Column(db.Integer, default=0)
    turnovers = db.Column(db.Integer, default=0)
    minutes_played = db.Column(db.Integer, default=0)

    game = db.relationship('Game', backref='stats')
