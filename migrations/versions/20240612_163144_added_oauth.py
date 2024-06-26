"""added oauth

Revision ID: cd4d4590fece
Revises:
Create Date: 2024-06-12 16:31:44.812691

"""
from alembic import op
import sqlalchemy as sa
import os
environment = os.getenv("FLASK_ENV")
SCHEMA = os.environ.get("SCHEMA")


# revision identifiers, used by Alembic.
revision = 'cd4d4590fece'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('places',
    sa.Column('id', sa.String(length=500), nullable=False),
    sa.Column('editorialSummary', sa.String(length=500), nullable=True),
    sa.Column('displayName', sa.String(length=100), nullable=True),
    sa.Column('types', sa.String(length=500), nullable=True),
    sa.Column('formattedAddress', sa.String(length=255), nullable=False),
    sa.Column('lat', sa.Numeric(), nullable=True),
    sa.Column('lng', sa.Numeric(), nullable=True),
    sa.Column('googleMapsUri', sa.String(length=1000), nullable=True),
    sa.Column('websiteUri', sa.String(length=1000), nullable=True),
    sa.Column('previewImage', sa.String(length=1000), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=40), nullable=False),
    sa.Column('first_name', sa.String(length=25), nullable=True),
    sa.Column('last_name', sa.String(length=25), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('lists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('shareable_by_link', sa.Boolean(), nullable=True),
    sa.Column('friends_view', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('place_id', sa.String(length=500), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('review', sa.String(length=800), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('list_reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('review_id', sa.Integer(), nullable=False),
    sa.Column('list_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['list_id'], ['lists.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['review_id'], ['reviews.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    if environment == "production":
        op.execute(f"ALTER TABLE users SET SCHEMA {SCHEMA};")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('list_reviews')
    op.drop_table('reviews')
    op.drop_table('lists')
    op.drop_table('users')
    op.drop_table('places')
    # ### end Alembic commands ###
