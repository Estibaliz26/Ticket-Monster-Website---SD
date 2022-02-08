from flask import Flask, g, current_app
from flask_restful import Resource, Api, reqparse
from data import *

from resources.orders import Orders
from resources.artists import Artist
from resources.artistList import ArtistList
from resources.ordersList import OrdersList
from resources.shows import Showy
from resources.showList import ShowList
from resources.login import Login
from resources.places import Place
from resources.placeList import PlaceList
from resources.accountsList import AccountsList
from resources.accounts import Accounts
from resources.placeShowList import PlaceShowsList
from resources.artistShowList import ArtistShowsList
from resources.showArtist import ShowArtist
from resources.showArtistList import ShowArtistsList

from datetime import datetime
from db import db, secret_key
from flask_migrate import Migrate
from models.artist import ArtistModel
from models.orders import OrdersModel
from models.accounts import AccountsModel
from models.orders import OrdersModel
from models.show import ShowModel  # also import table created with many-to-many relationship
from models.place import PlaceModel
from models.disciplines import DisciplineModel
from flask_cors import CORS
from flask import render_template
from decouple import config as config_decouple
from config import config

app = Flask(__name__,
            static_folder="frontend/dist/static",
            template_folder="frontend/dist")

'''
# Heroku 

app = Flask(__name__)
environment = config['development']
if config_decouple('PRODUCTION', cast=bool, default=False):
    environment = config['production']

app.config.from_object(environment)

'''

app.config.from_object(__name__)
api = Api(app)

app.config['SECRET_KEY'] = secret_key
CORS(app, resources={r'/*': {'origins': '*'}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

environment = config['development']

if config_decouple('PRODUCTION', cast=bool, default=False):
    environment = config['production']

app.config.from_object(environment)

migrate = Migrate(app, db, render_as_batch=True)

db.init_app(app)

api.add_resource(Orders, '/order/<string:username>')
api.add_resource(OrdersList, '/orders')

api.add_resource(Artist, '/artist/<int:id>', '/artist')
api.add_resource(ArtistList, '/artists')

api.add_resource(Showy, '/show/<int:id>', '/show')
api.add_resource(ShowList, '/shows')

api.add_resource(Place, '/place/<int:id>', '/place')
api.add_resource(PlaceList, '/places')

api.add_resource(ShowArtistsList, '/show/<int:id>/artists')
api.add_resource(ShowArtist, '/show/<int:id_show>/artist/<id_artist>', '/show/<int:id_show>/artist')

api.add_resource(ArtistShowsList, '/artist/<int:id>/shows')
api.add_resource(PlaceShowsList, '/place/<int:id>/shows')

api.add_resource(Accounts, '/account/<string:username>', '/account')
api.add_resource(AccountsList, '/accounts')

api.add_resource(Login, '/login')


@app.route('/')
def render_vue():
    return render_template("index.html")


@app.route('/python')
def like_python():
    return 'I like Python!'


@app.route('/artist/<int:id>', methods=['GET'])
def get_artist_id(id):
    return Artist.get(id)


@app.route('/artist', methods=['GET'])
@app.route('/artists', methods=['GET'])
def get_artists():
    return ArtistList.get()


@app.route('/show/<int:id>', methods=['GET'])
def get_show_id(id):
    return Showy.get(id)


@app.route('/shows', methods=['GET'])
@app.route('/show', methods=['GET'])
def get_shows():
    return ShowList.get()


@app.route('/place/<int:id>', methods=['GET'])
def get_place_id(id):
    return Place.get(id)


@app.route('/places', methods=['GET'])
@app.route('/place', methods=['GET'])
def get_places():
    return PlaceList.get()


@app.route('/order/<int:id>', methods=['GET'])
def get_order_id(id):
    return Orders.get(id)


@app.route('/order', methods=['GET'])
@app.route('/orders', methods=['GET'])
def get_orders():
    return OrdersList.get()


@app.route('/accounts/<int:id>', methods=['GET'])
def get_account_id(id):
    return Accounts.get(id)


@app.route('/account', methods=['GET'])
@app.route('/accounts', methods=['GET'])
def get_accounts():
    return AccountsList.get()


if __name__ == '__main__':
    app.run(port=5000, debug=True)
