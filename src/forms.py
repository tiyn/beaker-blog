import os

from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField, SubmitField, ValidationError, validators


def register_csrf(app):
  csrf = CSRFProtect()
  SECRET_KEY = os.urandom(32)
  app.secret_key = SECRET_KEY
  csrf.init_app(app)


class SearchForm(FlaskForm):
  query_str = StringField("Query", [validators.DataRequired("Please enter the search term")])
  # submit = SubmitField("Search")
