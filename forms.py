from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField, SubmitField,StringField
from wtforms.validators import Required, DataRequired, Length

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)


class BuyForm(Form):
   submit=SubmitField('Buy It')

class SearchForm(Form):
    search=TextField('search',validators=[Required()])

class CommentForm(Form):
    comment=TextAreaField('comment', validators=[Length(min=0, max=1000)])
    submit=SubmitField('Submit')