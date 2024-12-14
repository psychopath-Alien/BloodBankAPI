from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/bloodbank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Donors(db.Model):
    __tablename__='donors'
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(15), nullable=False)
    birthdate = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(45), nullable=False)
    BLOOD_BANKS_id = db.Column(db.Integer, db.ForeignKey('donors.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "dontaion_date": self.donation_date,
            "DONORS_id": self.DONORS_id
        }