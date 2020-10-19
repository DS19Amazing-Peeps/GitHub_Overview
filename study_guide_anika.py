from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

@APP.route('/')
def root():
    return "Hello, world!"

@APP.route('/game')
def game():
    game_id = 13
    url = 'https://www.boardgamegeek.com/xmlapi/boardgame/' + str(game_id)
    result = requests.get(url)
    soup = BeautifulSoup(result.text, features='lxml')

    return f"This game {soup.find('name').text} has {soup.find('minplayers').text}-{soup.find('maxplayers').text} players."

def get_info(game_id):
    url = 'https://www.boardgamegeek.com/xmlapi/boardgame/' + str(game_id)
    result = requests.get(url)
    soup = BeautifulSoup(result.text, features='lxml')   

    games = []
    game = game_id, (soup.find('name').text), (soup.find('maxplayers').text)
    games.append(game)

    return games

class Game(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(25))
    maxplayers = DB.Column(DB.Integer)

    def __repr__(self):
        return f'ID {self.id}, Name {self.name}, Max # of Players {self.maxplayers}'

@APP.route('/add/<game_id>')
def add(game_id):
    # info = [(13, "Catan", 5)]
    info = get_info(game_id)
    game = Game(id=info[0][0], name=info[0][1], maxplayers=info[0][2])
    DB.session.add(game)
    DB.session.commit()

    return "Game added!"

@APP.route('/reset')
def reset():
    DB.drop_all()
    DB.create_all()
    DB.session.commit()

    return "Database reset!"

@APP.route('/all')
def all():
    return str(Game.query.all())
