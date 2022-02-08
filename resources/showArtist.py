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


class ShowArtist(Resource):

    def get(self, id_artist, show_id):
        show = ShowModel.find_by_id(show_id)
        if show:
            for artist in show.artists:
                if artist.id == id_artist:
                    return artist.json(), 200

            return {'message': "Artist with id [{}] does not exist.".format(id_artist)}, 404

        else:
            return {'message': "Show with id [{}] does not exist.".format(show_id)}, 404

    #TODO: permissions?
    def post(self, id_show, id_artist=None):
        show = ShowModel.find_by_id(id_show)
        if show is None:
            return {"message": "Show with id [{}] does not exist".format(id_show)}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('country', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('disciplines', type=str,
                            action="append", required=True,
                            help="This field cannot be left blank")  # action = "append" is needed to

        try:
            data = parser.parse_args()
        except:
            return {"message": "Missing or wrongly formatted arguments."}, 400

        artist = ArtistModel.find_by_id(id_artist)
        if artist is not None:
            if artist.name != data["name"]:
                return {"message": "Artist ID already exists and does not match artist data"}, 400
        else:
            artist = ArtistModel.find_by_name(data["name"])
            if artist is None:
                artist = ArtistModel(data['name'], data['country'])
                for discipline_name in data['disciplines']:
                    discipline = DisciplineModel.find_by_name(discipline_name)
                    if discipline is None:
                        discipline = DisciplineModel(discipline_name)
                        discipline.save_to_db()
                    artist.disciplines.append(discipline)
                if id_artist is not None:
                    artist.id = id_artist

        if artist in show.artists:
            return {'message': "Artist with id [{}] already exists".format(id_artist)}, 409

        show.artists.append(artist)
        try:
            show.commit_to_db()
            return show.json(), 200
        except:
            return {"message": "An error occurred committing the changes to the show."}, 500

    def delete(self, id_show, id_artist=None):
        print('oloooo')
        show = ShowModel.find_by_id(id_show)
        if show is None:
            return {"message": "Show with id [{}] does not exist".format(id_show)}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=False)

        print('olooooooo')
        try:
            data = parser.parse_args()
        except:
            return {"message": "Missing or wrongly formatted arguments."}, 400

        if id_artist is not None:
            artist = ArtistModel.find_by_id(id_artist)
        elif data["name"] is not None:
            artist = ArtistModel.find_by_name(data["name"])
        else:
            return {'message': "At least one of artist id or name is required."}, 402

        if artist in show.artists:
            show.artists.remove(artist)
        else:
            return {'message': 'Artist not in show.'}, 404

        try:
            show.commit_to_db()
            return show.json(), 200
        except:
            return {"message": "An error occurred committing the changes to the show."}, 500
