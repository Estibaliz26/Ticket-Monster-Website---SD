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


class ShowArtistsList(Resource):
    def get(self, id):
        show = ShowModel.find_by_id(id)
        if show is None:
            return {"message": "Show with id [{}] does not exist".format(id)}, 404

        show_artists = [artist.json() for artist in show.artists]
        return {'artists': show_artists}, 200