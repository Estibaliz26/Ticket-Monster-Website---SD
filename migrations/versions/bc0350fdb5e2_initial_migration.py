"""Initial migration.

Revision ID: bc0350fdb5e2
Revises: 
Create Date: 2021-07-04 23:43:54.996368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc0350fdb5e2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accounts',
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('is_admin', sa.Integer(), nullable=False),
    sa.Column('available_money', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('username', name=op.f('pk_accounts')),
    sa.UniqueConstraint('username', name=op.f('uq_accounts_username'))
    )
    op.create_table('artists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('country', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_artists')),
    sa.UniqueConstraint('name', 'country', name=op.f('uq_artists_name')),
    sa.UniqueConstraint('name', name=op.f('uq_artists_name'))
    )
    op.create_table('disciplines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Enum('THEATRE', 'MUSIC', 'DANCE', 'CIRCUS', 'OTHER', 'CINEMA'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_disciplines'))
    )
    op.create_table('places',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('city', sa.String(length=30), nullable=False),
    sa.Column('country', sa.String(length=30), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_places')),
    sa.UniqueConstraint('name', 'city', 'country', 'capacity', name=op.f('uq_places_name'))
    )
    op.create_table('disciplines_in_artists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.Column('discipline_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], name=op.f('fk_disciplines_in_artists_artist_id_artists')),
    sa.ForeignKeyConstraint(['discipline_id'], ['disciplines.id'], name=op.f('fk_disciplines_in_artists_discipline_id_disciplines')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_disciplines_in_artists'))
    )
    op.create_table('orderss',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('id_show', sa.Integer(), nullable=False),
    sa.Column('tickets_bought', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['username'], ['accounts.username'], name=op.f('fk_orderss_username_accounts')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_orderss'))
    )
    op.create_table('shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('place_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('total_available_tickets', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], name=op.f('fk_shows_place_id_places')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_shows')),
    sa.UniqueConstraint('name', 'date', 'price', 'total_available_tickets', name=op.f('uq_shows_name')),
    sa.UniqueConstraint('name', name=op.f('uq_shows_name'))
    )
    op.create_table('artists_in_shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.Column('show_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], name=op.f('fk_artists_in_shows_artist_id_artists')),
    sa.ForeignKeyConstraint(['show_id'], ['shows.id'], name=op.f('fk_artists_in_shows_show_id_shows')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_artists_in_shows'))
    )
    op.create_table('places_in_shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('place_id', sa.Integer(), nullable=True),
    sa.Column('shows_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], name=op.f('fk_places_in_shows_place_id_places')),
    sa.ForeignKeyConstraint(['shows_id'], ['shows.id'], name=op.f('fk_places_in_shows_shows_id_shows')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_places_in_shows'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('places_in_shows')
    op.drop_table('artists_in_shows')
    op.drop_table('shows')
    op.drop_table('orderss')
    op.drop_table('disciplines_in_artists')
    op.drop_table('places')
    op.drop_table('disciplines')
    op.drop_table('artists')
    op.drop_table('accounts')
    # ### end Alembic commands ###