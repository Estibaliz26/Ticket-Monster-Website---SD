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


class Orders(Resource):

    def get(self, id):
        orders = [order.json() for order in OrdersModel.query.all() if order.id == id]
        if orders:
            return {'order': orders.json()}, 200

        else:
            return {'message': 'Order not found'}, 404

    @auth.login_required(role='user')
    def post(self, username):
        if g.user.username == username:
            parser = reqparse.RequestParser()  # create parameters parser from request

            # define all input parameters need and its type

            parser.add_argument('id_show', type=int, required=True, help="This field cannot be left blanck")
            parser.add_argument('tickets_bought', type=int, required=True, help="This field cannot be left blanck")

            data = parser.parse_args()
            new_order = OrdersModel(data['id_show'], data['tickets_bought'])

            for order in OrdersModel.query.all():
                if (order.id == id):
                    return {'message': "Order [{}] already exists.".format(id)}, 409

            if id is not None:
                new_order.id = id

            try:
                new_order.save_to_db()
                return new_order, 201

            except:
                return {"message": "An error occurred inserting the order."}, 500

        else:
            return {"message": "User not logged."}, 400

    @auth.login_required(role='user')
    def delete(self, id):
        for order in OrdersModel.query.all():
            if order.id == id:
                order.delete_from_db()
                return {'message': "Place with id [{}] removed".format(id)}, 200
        return {'message': "Order not found"}, 404

    @auth.login_required(role='user')
    def put(self, username):
        parser = reqparse.RequestParser()  # create parameters parser from request

        # define all input parameters need and its type
        parser.add_argument('id_show', type=int, required=True, help="This field cannot be left blanck")
        parser.add_argument('tickets_bought', type=int, required=True, help="This field cannot be left blanck")

        data = parser.parse_args()
        new_order = OrdersModel(data['id_show'], data['tickets_bought'])
        for order in OrdersModel.query.all():
            if order.id == id:
                order.username = new_order.username
                order.tickets_bought = new_order.tickets_bought
                order.save_to_db()
                return new_order.json(), 200
        try:
            new_order.save_to_db()
            return new_order.json(), 201
        except:
            return {"message": "An error occurred inserting the order."}, 500
