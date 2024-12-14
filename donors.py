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
            "gender": self.gender,
            "birthdate": self.birthdate,
            "name":  self.name,
            "contact": self.contact,
            "BLOOD_BANKS_id": self.BLOOD_BANKS_id,
            

        }
    
@app.route("/donor", methods=["GET"])
def get_all_donor():
    donors = Donors.query.all()
    return jsonify(
        {
            "success": True,
            "data": [donor.to_dict() for donor in donors]
        }
    ), 200
    

@app.route("/donor/<int:id>", methods=['GET'])
def get_single_donor(id):
    donors = db.session.get(Donors, id)
    if not donors:
        return jsonify(
            {
                "success": False,
                "error": "Donors not found"
            }
        ), 404
    return jsonify(
        {
            "success": True,
            "data": donors.to_dict()
        }
    ), 200

@app.route("/donor", methods=['POST'])
def add_donor():
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

    required_fields = ["gender", "birthdate", "name", "contact", "BLOOD_BANKS_id", "ADDRESS_id", "MEDICATIONS_code", "MEDICAL_CONDITIONS_code"]

    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing field: {field}"
                }
            ), 400

    try:
        new_donor = Donors(
           gender = data['gender'],
           birthdate = data['birthdate'],
           name = data['name'],
           contact = data['contact'],
           BLOOD_BANKS_id = data['BLOOD_BANKS_id'],
           ADDRESS_id = data['ADDRESS_id'],
           MEDICATIONS_code = data['MEDICATIONS_code']
           MEDICAL_CONDITIONS_code = data['MEDICAL_CONDITIONS_code']

       )
        db.session.add(new_donor)
        db.session.commit()
        return jsonify(
            {
                "success": True,
                "data": new_donor.to_dict()
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
    
@app.route("/donor/<int:id>", methods=["PUT"])
def update_donor(id):
    donor = db.session.get(Donors, id)
    if not donor:
        return jsonify(
            {
                "success": False,
                "error": "Donor not found"
            }
        ), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Invalid JSON"}), 400

    updatable_fields = ["id","gender", "birthdate", "name", "contact", "BLOOD_BANKS_id", "ADDRESS_id", "MEDICATIONS_code", "MEDICAL_CONDITIONS_code"]
    for field in updatable_fields:
        if field in data:
            setattr(donor, field, data[field])

    db.session.commit()
    return jsonify(
        {
            "success": True,
            "data": donor.to_dict()
        }
    ), 200

@app.route("/donor/<int:id>", methods=["DELETE"])
def delete_donor(id):
    donor = db.session.get(Donors, id)
    if not donor:
        return jsonify(
            {
                "success": False,
                "error": "Donors not found"
            }
        ), 404

    db.session.delete(donor)
    db.session.commit()
    return jsonify(
        {
            "success": True,
            "message": "Donor successfully deleted"
        }
    ), 200


if __name__ == '__main__':
    app.run(debug=True)