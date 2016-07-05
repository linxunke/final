from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
cart__shop = Table('cart__shop', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=80)),
    Column('intro', String(length=200)),
    Column('pic', String(length=256)),
    Column('views', Integer, default=ColumnDefault(0)),
    Column('orders', Integer, default=ColumnDefault(0)),
    Column('price', Float(precision=10)),
    Column('cartid', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['cart__shop'].columns['cartid'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['cart__shop'].columns['cartid'].drop()
