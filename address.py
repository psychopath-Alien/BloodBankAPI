from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/bloodbank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    country = db.Column(db.String(50), nullable=False)
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
def get_all_addresses():
    addresses = Address.query.all()
    return jsonify(
        {
            "success": True,
            "data": [add.to_dict() for add in addresses]
        }
    ), 200


@app.route("/address/<int:id>", methods=['GET'])
def get_single_address(id):
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


@app.route("/address", methods=['POST'])
def add_address():
    if not request.is_json:
        return jsonify(
            {
                "success": False,
                "error": "Content-type must be application/json"
            }
        ), 400

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Invalid JSON"}), 400

    required_fields = ["building_number", "street", "barangay", "city", "zipcode", "province", "country", "country_details"]
    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing field: {field}"
                }
            ), 400

    try:
        new_address = Address(
            building_number=data["building_number"],
            street=data["street"],
            barangay=data["barangay"],
            city=data["city"],
            zipcode=data["zipcode"],
            province=data["province"],
            country=data["country"],
            country_details=data["country_details"]
        )
        db.session.add(new_address)
        db.session.commit()
        return jsonify(
            {
                "success": True,
                "data": new_address.to_dict()
            }
        ), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "success": False,
                "error": str(e)
            }
        ), 500


@app.route("/address/<int:id>", methods=["PUT"])
def update_address(id):
    address = db.session.get(Address, id)
    if not address:
        return jsonify(
            {
                "success": False,
                "error": "Address not found"
            }
        ), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Invalid JSON"}), 400

    updatable_fields = ["building_number", "street", "barangay", "city", "zipcode", "province", "country", "country_details"]
    for field in updatable_fields:
        if field in data:
            setattr(address, field, data[field])

    db.session.commit()
    return jsonify(
        {
            "success": True,
            "data": address.to_dict()
        }
    ), 200


@app.route("/address/<int:id>", methods=["DELETE"])
def delete_address(id):
    address = db.session.get(Address, id)
    if not address:
        return jsonify(
            {
                "success": False,
                "error": "Address not found"
            }
        ), 404

    db.session.delete(address)
    db.session.commit()
    return jsonify(
        {
            "success": True,
            "message": "Address successfully deleted"
        }
    ), 200


if __name__ == '__main__':
    app.run(debug=True)
