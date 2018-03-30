from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, SearchPlayerForm

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


@app.route('/searched_list', methods=['GET', 'POST'])
def searched_list():
    flash('search player form submitted by {}'.format(request.form['player_name']))
    print("we are in request_player")
    print(request.form['player_name'])
    matched_players_list = search_a_player(request.form['player_name'])
    print(matched_players_list)
    return render_template('searched_list.html', title='found player list', player_list=matched_players_list)
    # return redirect(url_for('index'))


@app.route('/player_search', methods=['GET', 'POST'])
def request_player():
    form = SearchPlayerForm()
    return render_template('player_search.html', title='search players by name', form=form)


@app.route('/kohli', methods=['GET', 'POST'])
def kohli():
    virat_data = request_virat()
    return render_template('kohli.html', title='Kohli home', header_data=virat_data[0], stats_data=virat_data[1:])


@app.route('/dk', methods=['GET', 'POST'])
def dk():
    dk_data = request_dk()
    return render_template('kohli.html', title='Kohli home', header_data=dk_data[0], stats_data=dk_data[1:])


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


def search_a_player(player_name):
    r = requests.get("http://search.espncricinfo.com/ci/content/player/search.html?search=" + player_name)
    soup = BeautifulSoup(r.text, 'html.parser')
    players_list = soup.find_all("p", attrs={"class":"ColumnistSmry"})
    players_name_link = []
    import re
    for player in players_list:
        player_info = player.find("a")
        print(player_info)
        name = re.sub(r"[\\n\\t\s]*", "", player_info.contents[0].strip())
        cricinfo_link = player_info['href']
        #print('Name: {}, link: {}'.format(name, cricinfo_link))
        players_name_link.append({"name":name,"cricinfo_link":cricinfo_link})
    return players_name_link