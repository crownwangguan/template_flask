from flask import render_template
from . import main
from ..models import User
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.find_by_username(form.name.data)
        if user is None:
            user = User(username=form.name.data, password=form.password.data)
            user.save_to_db()
        else:
            return "<h1>User already exists.</h1>"
    return render_template('index.html', form=form)
