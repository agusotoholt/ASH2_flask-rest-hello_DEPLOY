from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

fav_chars = db.Table('fav_chars',
    db.Column('characters_id', db.Integer, db.ForeignKey('characters.id', ondelete='CASCADE'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
)

fav_planets = db.Table('fav_planets',
    db.Column('planets_id', db.Integer, db.ForeignKey('planets.id', ondelete='CASCADE'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
)

fav_ships = db.Table('fav_ships',
    db.Column('ships_id', db.Integer, db.ForeignKey('ships.id', ondelete='CASCADE'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)
    fav_chars = db.relationship('Characters', secondary = fav_chars, lazy = 'subquery', backref=db.backref('users', lazy=True, cascade='all, delete'))
    fav_planets = db.relationship('Planets', secondary = fav_planets, lazy = 'subquery', backref=db.backref('users', lazy=True, cascade='all, delete'))
    fav_ships = db.relationship('Ships', secondary = fav_ships, lazy = 'subquery', backref=db.backref('users', lazy=True, cascade='all, delete'))

    def __repr__(self):
        return '<User %r>' % self.username
    
    def serialize(self):
         return {
             "id": self.id,
             "username": self.username,
             "email": self.email,
             "is_active": self.is_active,
             # do not serialize the password, its a security breach
         }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    gender = db.Column(db.String(25), nullable=False)
    eye_color = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Characters %r>' % self.name
    
    def serialize(self):
         return {
             "id": self.id,
             "name": self.name,
             "gender": self.gender,
             "eye_color": self.eye_color,
             "age": self.age,
         }   

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    terrain = db.Column(db.String(50), nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    atmosphere = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
         return {
             "id": self.id,
             "name": self.name,
             "terrain": self.terrain,
             "diameter": self.diameter,
             "atmosphere": self.atmosphere,
         }   
    
class Ships(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    passengers = db.Column(db.Integer, nullable=False)
    manufacturer = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return '<Ships %r>' % self.name

    def serialize(self):
         return {
             "id": self.id,
             "name": self.name,
             "passengers": self.passengers,
             "manufacturer": self.manufacturer,
         }   