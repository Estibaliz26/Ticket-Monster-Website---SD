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

class OrdersList(Resource):

    def get(self, username):
        orders = [order.json() for order in OrdersModel.query.all()]
        return {'orders': orders}, 200 if orders else {'message': 'No orders found'}, 404

    @auth.login_required(role='user')
    def post(self, username):
        if g.user.username == username:
            parser = reqparse.RequestParser()
            parser.add_argument("orders_list", type=dict, action="append")
            data = parser.parse_args()
            total = 0

            for order in data["orders_list"]:
                for show in ShowModel.query.all():
                    if show.id == order['id_show']:
                        total += show.price

            if g.user.available_money > total:
                for order in data["orders_list"]:
                    new_order = OrdersModel(order['id_show'], order['tickets_bought'])
                    new_order.username = g.user.username
                    for show in ShowModel.query.all():
                        if show.total_available_tickets >= order['tickets_bought']:
                            show.total_available_tickets = show.total_available_tickets - order['tickets_bought']
                            g.user.available_money = g.user.available_money - show.price*order['tickets_bought']
                            g.user.orders.append(new_order)
                            db.session.add(new_order)
                            db.session.add(g.user)
                            db.session.add(show)
                            db.session.commit()
                            return new_order.json(), 201
            else:
                return {'message': 'Not enough money'}, 400

            return {'message': 'User Not found'}, 404

