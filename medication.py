from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/bloodbank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Medication(db.Model):
    __tablename__='medications'
    code = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    medication_other_details = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "medication_other_details": self.medication_other_details
        }
    
@app.route("/medication", methods=["GET"])
def get_all_medication():
    Med = Medication.query.all()
    return jsonify(
        {
            "success": True,
            "data": [med.to_dict() for med in Med]
        }
    ), 200

@app.route("/medication/<int:code>", methods=['GET'])
def get_single_medication(code):
    Med = db.session.get(Medication, code)
    if not Med:
        return jsonify(
            {
                "success": False,
                "error": "Medical Condition not found"
            }
        ), 404
    return jsonify(
        {
            "success": True,
            "data": Med.to_dict()
        }
    ), 200

@app.route("/medication", methods=['POST'])
def add_medication():
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

    required_fields = ["code", "name", "description", "medication_other_details"]

    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing field: {field}"
                }
            ), 400

    try:
        new_Med= Medication(
            code = data['code'],
            description = data['description'],
            medication_other_details = data['medication_other_details']

       )
        db.session.add(new_Med)
        db.session.commit()
        return jsonify(
            {
                "success": True,
                "data": new_Med.to_dict()
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
    
@app.route("/medication/<int:code>", methods=["PUT"])
def update_medication(code):
    Med = db.session.get(Medication, code)
    if not Med:
        return jsonify(
            {
                "success": False,
                "error": "Medical Condition not found"
            }
        ), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Invalid JSON"}), 400

    updatable_fields = ["code","description", "medication_other_details"]
    for field in updatable_fields:
        if field in data:
            setattr(Med, field, data[field])

    db.session.commit()
    return jsonify(
        {
            "success": True,
            "data": Med.to_dict()
        }
    ), 200

@app.route("/medication/<int:code>", methods=["DELETE"])
def delete_medication(id):
    Med = db.session.get(Medication, id)
    if not Med:
        return jsonify(
            {
                "success": False,
                "error": "Medication ot found"
            }
        ), 404

    db.session.delete(Med)
    db.session.commit()
    return jsonify(
        {
            "success": True,
            "message": "Medic successfully deleted"
        }
    ), 200


if __name__ == '__main__':
    app.run(debug=True)