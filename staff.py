from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/bloodbank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Staff(db.Model):
    __tablename__='staff'
    id = db.Column(db.Integer, primary_key=True)
    BLOOD_BANKS_id = db.Column(db.Integer, db.ForeignKey('blood_banks.id'), nullabe=False)
    ADDRESS_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    job_title = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(45), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "BLOOD_BANKS_id": self.BLOOD_BANKS_id,
            "ADDRESS_id": self.ADDRESS_id,
            "category": self.category,
            "gender": self.gender,
            "job_title": self.job_title,
            "name": self.name,
            "birthdate": self.birthdate.strftime("%Y-%m-%d")
        }
    
    
       