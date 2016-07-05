from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('nickname', VARCHAR(length=64)),
    Column('email', VARCHAR(length=120)),
    Column('role', SMALLINT),
    Column('about_me', VARCHAR(length=140)),
    Column('last_seen', DATETIME),
    Column('money', VARCHAR(length=64)),
)

shop = Table('shop', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=80)),
    Column('price', VARCHAR(length=30)),
    Column('intro', VARCHAR(length=200)),
    Column('pic', VARCHAR(length=256)),
    Column('views', INTEGER),
    Column('orders', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['money'].drop()
    pre_meta.tables['shop'].columns['price'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['money'].create()
    pre_meta.tables['shop'].columns['price'].create()
