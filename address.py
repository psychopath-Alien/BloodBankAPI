from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1/school'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == False

db = SQLAlchemy(app)

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    building_number = db.Column(db.String(20), nullable=False)
    street = db.Column(db.String(20), nullable=False)
    barangay = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(20), nullable=False)
    province = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nulllable=False)
    country_details = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "building_number": self.building_number,
            "street": self.street,
            "barangay": self.barangay,
            "city": self.city,
            "zipcode": self.zipcode,
            "province": self.province,
            "country": self.country,
            "country_details": self.country_details
        }

@app.route("/address", methods=["GET"])
def get_address():
    address = db.session.get(Address, id)
    if not address:
        return jsonify(
            {
                "success": False,
                "error": "Address not found"
            }
        ), 404
    return jsonify(
        {
            "success": True,
            "data": address.to_dict()
        }   
    ), 200