from .auth import auth_bp
from .dashboard import dashboard_bp
from .players import players_bp
from .teams import teams_bp
from .games import games_bp
from .core import core_bp  # ← Add this line
from .reports import reports_bp

__all__ = [
    'auth_bp',
    'dashboard_bp',
    'players_bp',
    'teams_bp',
    'games_bp',
    'core_bp',
    'reports_bp',
]
