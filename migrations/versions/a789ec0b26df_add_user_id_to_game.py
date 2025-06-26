"""Add user_id to Game

Revision ID: a789ec0b26df
Revises: a27437775b0b
Create Date: 2025-06-26 20:59:47.225375
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a789ec0b26df'
down_revision = 'a27437775b0b'
branch_labels = None
depends_on = None


def upgrade():
    # Add user_id to Game (nullable for now)
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_game_user_id', 'user', ['user_id'], ['id'])

    # Assign user_id to existing players dynamically (from team → user)
    op.execute("""
        UPDATE player
        SET user_id = (
            SELECT user.id
            FROM team
            JOIN user ON team.id = user.team_id
            WHERE team.id = player.team_id
        )
        WHERE user_id IS NULL;
    """)

    # Now safely make user_id non-nullable
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.alter_column('user_id',
            existing_type=sa.INTEGER(),
            nullable=False
        )
