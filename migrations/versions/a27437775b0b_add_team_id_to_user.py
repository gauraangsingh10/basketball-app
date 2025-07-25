"""Add team_id to User

Revision ID: a27437775b0b
Revises: 
Create Date: 2025-06-24 13:11:40.271076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a27437775b0b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
   with op.batch_alter_table('user', schema=None) as batch_op:
    batch_op.add_column(sa.Column('team_id', sa.Integer(), nullable=True))
    batch_op.create_foreign_key(
        'fk_user_team',  # ✅ Give the foreign key a name
        'team',
        ['team_id'],
        ['id']
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('team_id')

    # ### end Alembic commands ###
