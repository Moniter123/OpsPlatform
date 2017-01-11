"""empty message

Revision ID: 79bb8f337785
Revises: None
Create Date: 2016-12-07 11:07:41.472440

"""

# revision identifiers, used by Alembic.
revision = '79bb8f337785'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hostinfo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hostname', sa.String(length=32), nullable=True),
    sa.Column('public_ip', sa.String(length=32), nullable=True),
    sa.Column('private_ip', sa.String(length=32), nullable=True),
    sa.Column('mem_total', sa.String(length=32), nullable=True),
    sa.Column('cpu_type', sa.String(length=32), nullable=True),
    sa.Column('num_cpus', sa.Integer(), nullable=True),
    sa.Column('os_release', sa.String(length=32), nullable=True),
    sa.Column('kernelrelease', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('hostname')
    )
    op.create_table('random',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('num1', sa.String(length=12), nullable=True),
    sa.Column('num2', sa.String(length=12), nullable=True),
    sa.Column('num3', sa.String(length=12), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('random')
    op.drop_table('hostinfo')
    ### end Alembic commands ###
