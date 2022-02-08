from db import db


class OrdersModel(db.Model):
    __tablename__ = 'orderss'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), db.ForeignKey('accounts.username'), nullable=False)
    id_show = db.Column(db.Integer, nullable=False)
    tickets_bought = db.Column(db.Integer, nullable=False)

    def __init__(self, id_show, tickets_bought):
        self.id_show = id_show
        self.tickets_bought = tickets_bought

    def json(self):
        return {'username': self.username, 'id_show ': self.id_show, 'tickets_bought': self.tickets_bought}
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()