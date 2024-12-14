from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLACHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/bloodbank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class BloodBanks(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    blood_banks_details = db.Column(db.String(100), nullable=True)
    ADDRESS_id = db.Column(db.Integer, db.ForeignKey('address.ADDRESS_id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id, 
            "blood_banks_details": self.blood_banks_details,
            "ADDRESS_id": self.ADDRESS_id
        }
    
        
