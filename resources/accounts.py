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


class Accounts(Resource):

    def get(self, username=None):
        user = next((account for account in AccountsModel.query.all() if account.username == username), None)
        if user is not None:
            return {'account': user.json()}, 200
        else:
            return {'message': "Account not found"}, 404

    def post(self):

        parser = reqparse.RequestParser()

        try:
            parser.add_argument('username', type=str, required=True, help="This field cannot be blank")
            parser.add_argument('password', type=str, required=True, help="This field cannot be blank")
            parser.add_argument('money', type=int, required=False)
            parser.add_argument('admin', type=int, required=False)

            data = parser.parse_args()

            if data['admin'] and data['admin'] not in [0, 1]:
                return {"message": "Introduce a valid admin value."}, 400

            is_admin = 1 if data["admin"] and data["admin"] == 1 else 0

            if data["money"]:
                new_user = AccountsModel(data["username"], available_money=data["money"], is_admin=is_admin)
            else:
                new_user = AccountsModel(data["username"], is_admin=is_admin)
            new_user.hash_password(data['password'])
            new_user.save_to_db()

            return ({'account': new_user.json()}, 201) if new_user else (dict(), 404)

        except:
            return {"message": "An error occurred inserting the account."}, 500

    def delete(self, username=None):
        user = next((account for account in AccountsModel.query.all() if account.username == username), None)
        if user is not None:
            user.delete_from_db()
            return {'message': "Username with id [{}] removed".format(username)}, 200
        else:
            return {'message': "Username with id [{}] does not exist".format(username)}, 404

