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


class Place(Resource):

    def get(self, id=None):
        place = PlaceModel.find_by_id(id)
        if place is not None:
            return {'place': place.json()}, 200
        else:
            return {'message': "Place not found"}, 404

    def post(self, id=None):

        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, required=True, help="This field cannot be left blank")
            parser.add_argument('city', type=str, required=True, help="This field cannot be left blank")
            parser.add_argument('country', type=str, required=True, help="This field cannot be left blank")
            parser.add_argument('capacity', type=int, required=True, help="This field cannot be left blank")

            data = parser.parse_args()

            if PlaceModel.find_by_data(data["name"], data["city"], data["country"], data["capacity"]) is not None:
                return {'message': "Place with data [{}] already exists".format(data)}, 409
            if id is not None:
                for place in PlaceModel.query.all():
                    if place.id == id:
                        return {'message': "Place with id [{}] already exists".format(id)}, 409
            new_place = PlaceModel(data['name'], data['city'], data['country'], data['capacity'])

            if id is not None:
                new_place.id = id
                new_place.save_to_db()
                return new_place, 201
        except:
            return {"message": "An error occurred inserting the place."}, 500

    def delete(self, id=None):
        for place in PlaceModel.query.all():
            if place.id == id:
                place.delete_from_db()
                return {'message': "Place with id [{}] removed".format(id)}, 200

        return {'message': "Place with id [{}] does not exist".format(id)}, 404

    def put(self, id=None):
        parser = reqparse.RequestParser()  # create parameters parser from request
        parser.add_argument('name', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('city', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('country', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('capacity', type=int, required=True, help="This field cannot be left blank")
        data = parser.parse_args()
        place = PlaceModel.find_by_id(id)

        if place is None:
            return {"message": "Place with id [{}] does not exist".format(id)}, 404

        if data["name"]:
            place.name = data["name"]
        if data["city"]:
            place.city = data["city"]
        if data["country"]:
            place.country = data["country"]
        if data["capacity"]:
            place.capacity = data["capacity"]

        place.commit_to_db()

        return place.json(), 200
