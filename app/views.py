from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm, BuyForm, SearchForm, CommentForm
from models import User, Shop, Cart_Shop, Track, Mystore,Div,Resource, Comment, ROLE_USER, ROLE_ADMIN
from datetime import datetime
from config import  MAX_SEARCH_RESULTS
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user

    shops=Shop.query.order_by(Shop.name)



    return render_template('index.html',
        title = 'Home',
        user = user,
        shops=shops )

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])



@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user is None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))
    return render_template('user.html',
        user = user)

@app.route('/item/<id>', methods = ['GET', 'POST'])
@login_required
def item(id):
     user = g.user
     shop=Shop.query.filter_by(id=id).first()
     form=CommentForm()
     if form.validate_on_submit():
         q=Comment(name=g.user.nickname,comment=form.comment.data,item_id=id)
         db.session.add(q)
         db.session.commit()
         return redirect(url_for('index'))
     else:
         comments=Comment.query.filter_by(item_id=id)
     return render_template('item.html',
                            user=user,
                            shop=shop,
                            form=form,
                            comments=comments
                           )

@app.route('/transaction/<id>', methods = ['GET', 'POST'])
@login_required
def transaction(id):
    user=g.user
    shop=Shop.query.filter_by(id=id).first()
    form= BuyForm()
    if form.validate_on_submit():
         if g.user.money>shop.price:
             g.user.money=g.user.money-shop.price
             db.session.add(g.user)
             db.session.commit()
             q=Track(name=shop.name,pic=shop.pic,status='Ready to send',user_id=g.user.id )
             db.session.add(q)
             db.session.commit()
             return redirect(url_for('Success'))
         else :
             return redirect(url_for('false'))
    return render_template('transaction.html',
                           user=user,
                           form=form,
                           shop=shop)


@app.route('/Success')
@login_required
def Success():
    user=g.user
    return render_template('Success.html',
                           user=user)

@app.route('/false')
@login_required
def false():
    user=g.user
    return render_template('false.html',
                           user=user)

@app.route('/cart/<id>')
@login_required
def cart(id):
     if Cart_Shop.query.filter_by(user_id=g.user.id).first():
          shops=Cart_Shop.query.order_by(Cart_Shop.name)
     else:
         return redirect (url_for('cart_empty'))
     return render_template('cart.html',
                              shops=shops)

@app.route('/cart_empty')
@login_required
def cart_empty():

    return render_template('cart_empty.html')

@app.route('/put/<id>', methods = ['GET', 'POST'])
@login_required
def put(id):
    user=g.user
    if Cart_Shop.query.filter_by(shop_id=id).first() is None:
        cart=Shop.query.filter_by(id=id).first()
        q=Shop.query.filter_by(id=cart.id).first()
        l=Cart_Shop(name=q.name,intro=q.intro,pic=q.pic,views=q.views,orders=q.orders,price=q.price,shop_id=id,user_id=g.user.id)
        db.session.add(l)
        db.session.commit()

    else:
         flash('It has existed.')
    return render_template('put.html',
                           user=user)


@app.route('/remove/<id>', methods = ['GET', 'POST'])
@login_required
def remove(id):
    q=Cart_Shop.query.filter_by(shop_id=id).first()
    db.session.delete(q)
    db.session.commit()
    return render_template ('remove.html')

@app.before_request
def before_request():
    g.user=current_user
    if g.user.is_authenticated:
        g.user.last_seen=datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form=SearchForm()

@app.route('/search', methods = ['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query = g.search_form.search.data))


@app.route('/search_results/<query>')
@login_required
def search_results(query):
    shops = Shop.query.filter(Shop.intro.like("%"+query+"%")).all()
    return render_template('search_results.html',
        query = query,
        shops = shops)


@app.route('/track')
@login_required
def track():
    tracks=Track.query.filter_by(user_id=g.user.id).all()
    return render_template('track.html',
                           tracks=tracks)


@app.route('/putstore/<id>', methods = ['GET', 'POST'])
@login_required
def putstore(id):
    user=g.user
    if Mystore.query.filter_by(shop_id=id).first() is None:
        mystore=Shop.query.filter_by(id=id).first()
        q=Shop.query.filter_by(id=mystore.id).first()
        l=Mystore(name=q.name,intro=q.intro,pic=q.pic,views=q.views,orders=q.orders,price=q.price,shop_id=id,user_id=g.user.id)
        db.session.add(l)
        db.session.commit()

    else:
         flash('It has existed.')
    return render_template('putstore.html',
                           user=user)

@app.route('/removestore/<id>', methods = ['GET', 'POST'])
@login_required
def removestore(id):
    q=Mystore.query.filter_by(shop_id=id).first()
    db.session.delete(q)
    db.session.commit()
    return render_template ('removestore.html')

@app.route('/mystore/<id>')
@login_required
def mystore(id):
     if Mystore.query.filter_by(user_id=g.user.id).first():
         mystores=Mystore.query.order_by(Mystore.name)
     else:
         return redirect (url_for('store_empty'))

     if Resource.query.order_by(Resource.name) is None:
         return redirect (url_for('div'))
     else:
         resource=Resource.query.filter_by(user_id=g.user.id).first()
     return render_template('mystore.html',
                              mystores=mystores,
                            resource=resource
                            )

@app.route('/store_empty')
@login_required
def store_empty():

    return render_template('store_empty.html')

@app.route('/putdecorate/<id>', methods = ['GET', 'POST'])
@login_required
def putdecorate(id):
     user=g.user
     if Resource.query.filter_by(div_id=id).first() is None:
          div=Div.query.filter_by(id=id).first()
          q=Div.query.filter_by(id=div.id).first()
          l=Resource(div_id=id,name=q.name,pic=q.pic,user_id=g.user.id)
          db.session.add(l)
          db.session.commit()
     return render_template('putdecorate.html',
                            user=user)


@app.route('/div')
@login_required
def div():
    divs=Div.query.order_by(Div.name)

    return render_template('div.html',
                           divs=divs)



@app.route('/removedecorate/<id>', methods = ['GET', 'POST'])
@login_required
def removedecorate(id):
    q=Resource.query.filter_by(div_id=id).first()
    db.session.delete(q)
    db.session.commit()
    return render_template ('removedecorate.html')

@app.route('/contact')
@login_required
def contact():

    return render_template('contact.html')