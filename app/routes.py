from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

from bs4 import BeautifulSoup
import requests

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


@app.route('/kohli', methods=['GET', 'POST'])
def kohli():
    virat_data = request_virat()
    return render_template('kohli.html', title='Kohli home', data=virat_data)

@app.route('/dk', methods=['GET', 'POST'])
def dk():
    dk_data = request_dk()
    return render_template('kohli.html', title='Kohli home', data=dk_data)

def request_virat():
    url_virat="http://www.espncricinfo.com/india/content/player/253802.html"
    return get_player_data(url_virat)

def request_dk():
    url_dk="http://www.espncricinfo.com/india/content/player/30045.html"
    return get_player_data(url_dk)

def get_player_data(player_url):
    r = requests.get(player_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find("table", attrs={"class":"engineTable"})
    player_data = extract_data(table.find('tr', attrs={"class":"head"}).find_all("th"))
    allData = table.find_all('tr', attrs={"class":"data1"})
    return [player_data] + [extract_data(another_format_data.find_all("td")) for another_format_data in allData]

def extract_data(data):
    return [ each_data_element.get_text().strip() for each_data_element in data]