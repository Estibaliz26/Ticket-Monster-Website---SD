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


class Artist(Resource):

    def get(self, id=None):
        artists = next((artist for artist in ArtistModel.query.all() if artist.id == id), None)
        if artists is not None:
            return {'artist': artists.json()}, 200
        else:
            return {'message': "Artist not found"}, 404

    def post(self, id=None):

        try:
            if id is not None:
                for artist in ArtistModel.query.all():
                    if artist.id == id:
                        return {'message': "Artist with id [{}] already exists".format(id)}, 409

            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, required=True, help="This field cannot be left blank")
            parser.add_argument('country', type=str, required=True, help="This field cannot be left blank")
            parser.add_argument('disciplines', type=str,
                                action="append", required=True,
                                help="This field cannot be left blank")  # action = "append" is needed to determine that is a list of strings

            data = parser.parse_args()
            new_artist = ArtistModel(data['name'], data['country'])

            for discipline in data['disciplines']:
                dis = DisciplineModel.find_by_name(discipline)
                if dis is None:
                    dis = DisciplineModel(discipline)
                artist.disciplines.append(dis)

            if id is not None:
                new_artist.id = id

            new_artist.save_to_db()
            return new_artist.json(), 201

        except:
            return {"message": "An error occurred inserting the artist."}, 500


    def delete(self, id=None):

        if id is None:
            return {'message': "Introduce Id"}, 400

        for artist in ArtistModel.query.all():
            if artist.id == id:
                artist.delete_from_db()
                return {'message': "Artist with id [{}] removed".format(id)}, 200

        return {'message': "Artist with id [{}] does not exist".format(id)}, 404

    def put(self, id=None):

        try:
            parser = reqparse.RequestParser()

            parser.add_argument('name', type=str, required=True, help="This field cannot be left blanck")
            parser.add_argument('country', type=str, required=True, help="This field cannot be left blanck")
            parser.add_argument('disciplines', type=str,
                                action="append", required=True,
                                help="This field cannot be left blanck")  # action = "append" is needed to determine that is a list of strings

            data = parser.parse_args()

            artist = ArtistModel.find_by_id(id)
            if artist is None:
                return {"message": "Artist with id [{}] does not exist".format(id)}, 404

            if data["name"]:
                artist.name = data["name"]
            if data["country"]:
                artist.country = data["country"]
            if data["disciplines"]:
                artist.name = data["name"]
                artist.disciplines = []
                for discipline in data['disciplines']:
                    dis = DisciplineModel.find_by_name(discipline)
                    if dis is None:
                        dis = DisciplineModel(discipline)
                    artist.disciplines.append(dis)
            artist.commit_to_db()
            return artist.json(), 200
        except:
            return {"message": "An error occurred inserting the artist."}, 500
