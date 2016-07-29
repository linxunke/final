from hashlib import md5
from app import db
from app import app
import flask.ext.whooshalchemy as whooshalchemy

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    money=db.Column(db.Float(10))
    cart_user = db.relationship('Cart_Shop', backref = 'user', lazy = 'dynamic')
    track_item = db.relationship('Track', backref = 'user', lazy = 'dynamic')
    mystore_user=db.relationship('Mystore', backref = 'user', lazy = 'dynamic')
    resource_user=db.relationship('Resource', backref = 'user', lazy = 'dynamic')
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email.encode('utf-8')).hexdigest() + '?d=mm&s=' + str(size)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

class Shop(db.Model):
    __searchable__=['intro']
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String (80))
    intro =db.Column(db.String(200))
    pic = db.Column(db.String(256))
    views = db.Column(db.Integer,default = 0)
    orders = db.Column(db.Integer,default = 0)
    price=db.Column(db.Float(10))
    comment_shopr=db.relationship('Comment', backref = 'shop', lazy = 'dynamic')
    def __repr__(self):
        return '<Shop %r>' % (self.name)

whooshalchemy.whoosh_index(app, Shop)




class Cart_Shop(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String (80))
    intro =db.Column(db.String(200))
    pic = db.Column(db.String(256))
    views = db.Column(db.Integer,default = 0)
    orders = db.Column(db.Integer,default = 0)
    price=db.Column(db.Float(10))
    shop_id=db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Cart_Shop %r>' % (self.name)

class Track(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String (80))
    pic = db.Column(db.String(256))
    status = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Track %r>' % (self.name)

class Mystore(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String (80))
    intro =db.Column(db.String(200))
    pic = db.Column(db.String(256))
    views = db.Column(db.Integer,default = 0)
    orders = db.Column(db.Integer,default = 0)
    price=db.Column(db.Float(10))
    shop_id=db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Mystore %r>' % (self.name)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    div_id = db.Column(db.String (80))
    name = db.Column(db.String (80))
    pic = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
      return '<Resource %r>' % (self.name)

class Div(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String (80))
    pic = db.Column(db.String(256))

    def __repr__(self):
      return '<Div %r>' % (self.name)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name=db.Column(db.String (80))
    comment = db.Column(db.String (1000))
    item_id = db.Column(db.Integer, db.ForeignKey ('shop.id'))

    def __repr__(self):
        return '<Comment %r>' % (self.name)