from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Abhijeet'}
    posts = [{'user':'Abhi', 'message':'Advait here is for the world'},
            {'user':'Mohan', 'message':'Everything is just one and only one'}]
    return render_template('index.html', title='Kislay home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # This setting gets validated during a POST request
    if form.validate_on_submit():
        flash('user login form submitted by {}'.format(form.username.data))
        return redirect(url_for('index'))
    else:
        return render_template('login.html', title='Sign In', form=form)