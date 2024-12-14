from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/bloodbank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class BloodBanks(db.Model):
    __tablename__ = 'blood_banks'
    id = db.Column(db.Integer, primary_key=True)
    blood_bank_details = db.Column(db.String(100), nullable=True)
    ADDRESS_id = db.Column(db.Integer, db.ForeignKey('address.ADDRESS_id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id, 
            "blood_bank_details": self.blood_bank_details,
            "ADDRESS_id": self.ADDRESS_id
        }

@app.route("/bloodbank", methods=["GET"])
def get_all_bloodbanks():
    bloodbanks = BloodBanks.query.all()
    return jsonify(
        {
            "success": True,
            "data": [bloodbank.to_dict() for bloodbank in bloodbanks]
        }
    ), 200


@app.route("/bloodbank/<int:id>", methods=['GET'])
def get_single_bloodbank(id):
    bloodbank= db.session.get(BloodBanks, id)
    if not bloodbank:
        return jsonify(
            {
                "success": False,
                "error": "Blood Bank not found"
            }
        ), 404
    return jsonify(
        {
            "success": True,
            "data": bloodbank.to_dict()
        }
    ), 200

@app.route("/bloodbank", methods=['POST'])
def add_bloodbank():
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

    required_fields = ["blood_bank_details", "ADDRESS_id"]
    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing field: {field}"
                }
            ), 400

    try:
        new_bloodbank = BloodBanks(
            blood_bank_details = data['blood_bank_details'],
            ADDRESS_id = data['ADDRESS_id']
        )
        db.session.add(new_bloodbank)
        db.session.commit()
        return jsonify(
            {
                "success": True,
                "data": new_bloodbank.to_dict()
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
    
@app.route("/bloodbanks/<int:id>", methods=["PUT"])
def update_bloodbanks(id):
    bloodbank = db.session.get(BloodBanks, id)
    if not bloodbank:
        return jsonify(
            {
                "success": False,
                "error": "Blood Banks not found"
            }
        ), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Invalid JSON"}), 400

    updatable_fields = ["id", "blood_bank_details", "ADDRESS_id"]
    for field in updatable_fields:
        if field in data:
            setattr(bloodbank, field, data[field])

    db.session.commit()
    return jsonify(
        {
            "success": True,
            "data": bloodbank.to_dict()
        }
    ), 200

@app.route("/bloodbanks/<int:id>", methods=["DELETE"])
def delete_bloodbanks(id):
    bloodbank= db.session.get(BloodBanks, id)
    if not bloodbank:
        return jsonify(
            {
                "success": False,
                "error": "Nlood Bank not found"
            }
        ), 404

    db.session.delete(bloodbank)
    db.session.commit()
    return jsonify(
        {
            "success": True,
            "message": "Blood bank successfully deleted"
        }
    ), 200


if __name__ == '__main__':
    app.run(debug=True)
