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
from models.accounts import auth


class Showy(Resource):  # Si se usa Show salta una excepcion, segun informacion de internet es un bug de flask-restplus

    def get(self, id=None):
        shows = ShowModel.query.get(id)
        if shows is not None:
            return {'shows': shows.json()}, 200
        else:
            return {'message': "Show not found"}, 404

    @auth.login_required(role='admin')
    def post(self, id=None):
        parser = reqparse.RequestParser()  # create parameters parser from request

        # define all input parameters need and its type

        parser.add_argument('name', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('date', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('price', type=float, required=True, help="This field cannot be left blank")
        parser.add_argument('place', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('city', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('country', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('total_available_tickets', type=int, required=True, help="This field cannot be left blank")
        parser.add_argument('artists', type=str, action="append", required=False) # unused in practice

        try:
            data = parser.parse_args()
            isodate = datetime.strptime(data['date'], "%Y-%m-%d")
        except:
            return {"message": "Missing or wrongly formatted arguments."}, 400

        place = PlaceModel.find_by_data(data["place"], data["city"], data["country"], data["total_available_tickets"])
        if place is None:
            place = PlaceModel(data["place"], data["city"], data["country"], data["total_available_tickets"])
            place.save_to_db()

        if data["total_available_tickets"] < 0:
            return {"message": "amount of tickets specified cannot be negative"}, 500

        if data["price"] < 0:
            return {"message": "entry fee cannot be negative"}, 500

        new_show = ShowModel(data['name'], isodate, data['price'], place.id, data["total_available_tickets"])

        if data["artists"] is None:
            data["artists"] = []
        for artist_name in data["artists"]:
            artist = ArtistModel.find_by_name(artist_name)
            if artist is None:
                return {"message": "artist name [{}] recieved does not \
                                    correspond to any artist in the db".format(artist_name)}, 401
            new_show.artists.append(artist)

        if id is not None:
            if ShowModel.find_by_id(id) is not None:
                return {"message": "there already exists a show with the passed id [{}]".format(id)}, 402
            new_show.id = id
        try:
            new_show.save_to_db()
            return new_show.json(), 201
        except:
            return {"message": "An error occurred inserting the show."}, 500

    @auth.login_required(role='admin')
    def delete(self, id=None):
        shows = ShowModel.find_by_id(id)
        if shows is None:
            return {'message': "Show with id [{}] does not exist".format(id)}, 404
        shows.delete_from_db()
        return {'message': "Show with id [{}] removed".format(id)}, 200

    @auth.login_required(role='admin')
    def put(self, id=None):

        show = ShowModel.find_by_id(id)
        if show is None:
            return {"message": "Show with id [{}] does not exist".format(id)}, 404

        parser = reqparse.RequestParser()  # create parameters parser from request

        parser.add_argument('name', type=str, required=False)
        parser.add_argument('price', type=float, required=False)
        parser.add_argument('country', type=str, required=False)
        parser.add_argument('date', type=str, required=False)
        parser.add_argument('place', type=str, required=False)
        parser.add_argument('city', type=str, required=False)
        parser.add_argument('total_available_tickets', type=int, required=False)
        parser.add_argument('artists', type=str, action="append", required=False) # unused in practice

        try:
            data = parser.parse_args()
            isodate = datetime.strptime(data['date'], "%Y-%m-%d")
        except:
            return {"message": "Missing or wrongly formatted arguments."}, 400

        if data["name"]:
            show.name = data["name"]
        if data["price"]:
            show.price = data["price"]
        if data["date"]:
            show.date = isodate
        if data["total_available_tickets"]:
            show.total_available_tickets = data["total_available_tickets"]

        if data["artists"]:
            show.artists = []
            for artist_name in data["artists"]:
                artist = ArtistModel.find_by_name(artist_name)
                if artist is None:
                    return {"message": "artist name [{}] recieved does not \
                                        correspond to any artist in the db".format(artist_name)}, 401
                show.artists.append(artist)

        new_city = data["city"] if data["city"] is not None else PlaceModel.find_by_id(show.place_id).city
        new_place = data["place"] if data["place"] is not None else PlaceModel.find_by_id(show.place_id).name
        new_country = data["country"] if data["country"] is not None else PlaceModel.find_by_id(show.place_id).country
        new_capacity = data["total_available_tickets"] if data["total_available_tickets"] is not None \
                       else PlaceModel.find_by_id(show.place_id).capacity

        place = PlaceModel.find_by_data(new_place, new_city, new_country, new_capacity)
        if place is None:
            place = PlaceModel(new_place, new_city, new_country, new_capacity)
            place.save_to_db()
        new_id = place.id

        show.place_id = new_id # might not change anything

        try:
            show.commit_to_db()
            return show.json(), 200
        except:
            return {"message": "An error occurred committing the changes to the show."}, 500
