from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
cart = Table('cart', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('shop_id', Integer),
    Column('user_id', Integer),
)

shop = Table('shop', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=80)),
    Column('intro', VARCHAR(length=200)),
    Column('pic', VARCHAR(length=256)),
    Column('views', INTEGER),
    Column('orders', INTEGER),
    Column('price', FLOAT),
    Column('user_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['cart'].create()
    pre_meta.tables['shop'].columns['user_id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['cart'].drop()
    pre_meta.tables['shop'].columns['user_id'].create()
