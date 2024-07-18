"""Post model

Revision ID: e650390b986d
Revises: 06e57655c513
Create Date: 2024-06-26 00:41:03.862344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e650390b986d'
down_revision = '06e57655c513'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=150), nullable=True),
    sa.Column('date_create', sa.DateTime(), nullable=True),
    sa.Column('date_deletion', sa.DateTime(), nullable=True),
    sa.Column('privacy', sa.Boolean(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('syntax', sa.String(), nullable=True),
    sa.Column('post_text', sa.Text(), nullable=True),
    sa.Column('url_post_text', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    # ### end Alembic commands ###
