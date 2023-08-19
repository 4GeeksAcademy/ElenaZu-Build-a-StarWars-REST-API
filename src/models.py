from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship("Favorite", backref = "user", uselist = True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model) :
    id = db.Column(db.Integer, primary_key=True) 
    description = db.Column(db.String(300))
    name = db.Column(db.String(50), nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    terrain = db.Column(db.String(50), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "descriptcion": self.description,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "terrain": self.terrain   
        }

class Character(db.Model) :
    id = db.Column(db.Integer, primary_key=True)     
    description = db.Column(db.String(300))
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50),nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    skin_color = db.Column(db.String(10),nullable=False)
    eye_color = db.Column(db.String(10),nullable=False)
    planet_id =  db.Column(db.Integer, db.ForeignKey("planet.id"))
    planet = db.relationship("Planet")
    
    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "mass": self.mass,
            "height": self.height,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "planet_id": self.planet_id
        }


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    __table_args__= (db.UniqueConstraint(
        'user_id',
        'name',
        name= 'favorite_unique'
    ),)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id
        }
    
    @classmethod
    def create(cls,favorite):
        try:
            new_favorite = cls(**favorite)
            db.session.add(new_favorite)
            db.session.commit()
            return new_favorite
        except Exception as error:
            print(error)
            db.session.rollback() 
            return None

