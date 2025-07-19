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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    user = db.relationship('User', backref='games')

class Stat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))

    # Scoring
    two_pointers = db.Column(db.Integer, default=0)
    three_pointers = db.Column(db.Integer, default=0)
    free_throws = db.Column(db.Integer, default=0)

    # Calculated manually for now
    points = db.Column(db.Integer, default=0)

    # Playmaking
    assists = db.Column(db.Integer, default=0)
    converted_assists = db.Column(db.Integer, default=0)
    missed_assists = db.Column(db.Integer, default=0)

    # Rebounds
    off_rebounds = db.Column(db.Integer, default=0)
    def_rebounds = db.Column(db.Integer, default=0)

    # Defense
    steals = db.Column(db.Integer, default=0)
    blocks = db.Column(db.Integer, default=0)

    # Fouls and Violations
    personal_fouls = db.Column(db.Integer, default=0)
    unsportsmanlike_fouls = db.Column(db.Integer, default=0)
    three_sec_violations = db.Column(db.Integer, default=0)
    five_sec_violations = db.Column(db.Integer, default=0)

    # Turnovers
    bad_passes = db.Column(db.Integer, default=0)
    traveling = db.Column(db.Integer, default=0)

    turnovers = db.Column(db.Integer, default=0)  # May auto-calculate from others
    minutes_played = db.Column(db.Integer, default=0)

    game = db.relationship('Game', backref='stats')

    @property
    def total_rebounds(self):
        return self.off_rebounds + self.def_rebounds
    
    @property 
    def points(self):
        return (
            self.two_pointers * 2 +
            self.three_pointers * 3 +
            self.free_throws
        )

    @property
    def total_fouls(self):
        return self.personal_fouls + self.unsportsmanlike_fouls

    @property
    def total_turnovers(self):
        return (
            self.turnovers +
            self.three_sec_violations +
            self.five_sec_violations +
            self.bad_passes +
            self.traveling
        )

    @property
    def rating(self):
        return (
            self.points * 1 +
            self.total_rebounds * 1.2 +
            self.assists * 1.5 +
            self.steals * 3 +
            self.blocks * 3 -
            self.total_turnovers * 2 -
            self.total_fouls * 1
        )
