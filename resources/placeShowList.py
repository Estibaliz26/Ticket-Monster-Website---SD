from flask import Flask, g
from flask_restful import Resource, Api, reqparse
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


class PlaceShowsList(Resource):
    def get(self, id):
        place = PlaceModel.find_by_id(id)
        if place:
            #TODO
            shows = [show.json() for show in ShowModel.query.all() for place in show.get_places_from_show if
                     place.id == id]
            if shows:
                return {'shows': shows}, 200
            else:
                return {'message': "No shows found"}, 404
        else:
            return {'message': 'No places found'}, 404
