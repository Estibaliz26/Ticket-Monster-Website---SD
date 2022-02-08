from db import db
import dateutil.parser

from models.place import PlaceModel

artists_in_shows = db.Table('artists_in_shows',
                            db.Column('id', db.Integer, primary_key=True),
                            db.Column('artist_id', db.Integer, db.ForeignKey('artists.id')),
                            db.Column('show_id', db.Integer, db.ForeignKey('shows.id')))

places_in_shows = db.Table('places_in_shows',
                           db.Column('id', db.Integer, primary_key=True),
                           db.Column('place_id', db.Integer, db.ForeignKey('places.id')),
                           db.Column('shows_id', db.Integer, db.ForeignKey('shows.id')))


class ShowModel(db.Model):
    __tablename__ = 'shows'  # This is table name
    __table_args__ = (db.UniqueConstraint('name', 'date', 'price', 'total_available_tickets'),)

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    name = db.Column(db.String(30), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    artists = db.relationship("ArtistModel", secondary=artists_in_shows, backref=db.backref('shows'))
    total_available_tickets = db.Column(db.Integer)

    def __init__(self, name, date, price, place_id, tickets):
        self.name = name
        self.date = date
        self.price = price
        self.total_available_tickets = tickets
        self.place_id = place_id
        self.artists = []

    def get_artists_from_show(self):
        if self.artists:
            return {'artists': self.artists}
        return {'artists': []}

    def json(self):
        artists = []
        if self.artists:
            artists = [artist.json() for artist in self.artists]
        _,month,etc = self.date.isoformat().split("-")
        month = ["JAN","FEB","MAR","ABR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"][int(month)-1]
        day,_ = etc.split("T")
        place = PlaceModel.find_by_id(self.place_id)
        return {'id': self.id,
                'place': place.json() if place is not None else None,
                'name': self.name,
                'date': self.date.isoformat(),
                'month': month, 'day': day,
                'price': self.price,
                'total_available_tickets': self.total_available_tickets,
                'artists': artists}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).all()
