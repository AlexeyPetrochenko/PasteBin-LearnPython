"""Comment

Revision ID: 7ab5b9ad153b
Revises: 2aa7f370296e
Create Date: 2024-07-16 01:21:50.766165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ab5b9ad153b'
down_revision = '2aa7f370296e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('context', sa.Text(), nullable=False),
    sa.Column('time_comment', sa.DateTime(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('coments', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_coments_post_id'), ['post_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_coments_user_id'), ['user_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('coments', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_coments_user_id'))
        batch_op.drop_index(batch_op.f('ix_coments_post_id'))

    op.drop_table('coments')
    # ### end Alembic commands ###
