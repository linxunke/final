from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField, SubmitField,StringField
from wtforms.validators import Required, Length

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)


class BuyForm(Form):
   submit=SubmitField('Buy It')

class SearchForm(Form):
    search=TextField('search',validators=[Required()])