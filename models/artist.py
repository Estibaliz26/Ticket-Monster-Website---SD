from db import db

disciplines_in_artists = db.Table('disciplines_in_artists',
                                  db.Column('id', db.Integer, primary_key=True),
                                  db.Column('artist_id', db.Integer, db.ForeignKey('artists.id')),
                                  db.Column('discipline_id', db.Integer, db.ForeignKey('disciplines.id')))


class ArtistModel(db.Model):
    __tablename__ = 'artists'  # This is table name
    __table_args__ = (db.UniqueConstraint('name', 'country'),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    country = db.Column(db.String(30), nullable=False)
    disciplines = db.relationship("DisciplineModel", secondary=disciplines_in_artists, backref=db.backref('artists'))

    def __init__(self, name, country):
        self.name = name
        self.country = country

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def json(self):
        return {'id': self.id, 'name': self.name, 'country': self.country,
                'disciplines': [discipline.json() for discipline in self.disciplines]}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()
