import sqlalchemy as s

from database import database, metadata


users = s.Table(
    'users',
    metadata,
    s.Column('id', s.Integer, primary_key=True),
    s.Column('email', s.String),
    s.Column('password', s.String),
)