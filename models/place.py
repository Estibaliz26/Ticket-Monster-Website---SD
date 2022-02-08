from db import db


class PlaceModel(db.Model):
    __tablename__ = 'places'  # This is table name
    __table_args__ = (db.UniqueConstraint('name', 'city', 'country', 'capacity'),)

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(30), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    def __init__(self, name, city, country, capacity):
        self.name = name
        self.city = city
        self.country = country
        self.capacity = capacity

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def find_by_data(cls, name, city, country, capacity):
        return cls.query.filter_by(name=name, city=city, country=country, capacity=capacity).first()

    def json(self):
        return {'id': self.id, 'name': self.name, 'country': self.country, 'city': self.city, 'capacity': self.capacity}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()
