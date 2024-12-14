from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/bloodbank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Donation(db.Model):
    __tablename__='donations'
    id = db.Column(db.Integer, primary_key=True)
    donation_date = db.Column(db.String(45), nullable=False)
    DONORS_id = db.Column(db.Integer, db.ForeignKey('donors.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "dontaion_date": self.donation_date,
            "DONORS_id": self.DONORS_id
        }
    
@app.route("/donation", methods=["GET"])
def get_all_donation():
    donations = Donation.query.all()
    return jsonify(
        {
            "success": True,
            "data": [donate.to_dict() for donate in donations]
        }
    ), 200
    

@app.route("/donation/<int:id>", methods=['GET'])
def get_single_donation(id):
    donation = db.session.get(Donation, id)
    if not donation:
        return jsonify(
            {
                "success": False,
                "error": "Donation not found"
            }
        ), 404
    return jsonify(
        {
            "success": True,
            "data": donation.to_dict()
        }
    ), 200

@app.route("/donation", methods=['POST'])
def add_donation():
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

    required_fields = ["donation_date","DONORS_id"]
    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing field: {field}"
                }
            ), 400

    try:
        new_donation = Donation(
            donation_date = data['donation_date'],
            DONORS_id = data['DONORS_id']
       )
        db.session.add(new_donation)
        db.session.commit()
        return jsonify(
            {
                "success": True,
                "data": new_donation.to_dict()
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
    
@app.route("/donation/<int:id>", methods=["PUT"])
def update_donation(id):
    donation = db.session.get(Donation, id)
    if not donation:
        return jsonify(
            {
                "success": False,
                "error": "Donation not found"
            }
        ), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Invalid JSON"}), 400

    updatable_fields = ["id","donation_date", "DONORS_id"]
    for field in updatable_fields:
        if field in data:
            setattr(donation, field, data[field])

    db.session.commit()
    return jsonify(
        {
            "success": True,
            "data": donation.to_dict()
        }
    ), 200

@app.route("/donation/<int:id>", methods=["DELETE"])
def delete_donation(id):
    donation= db.session.get(Donation, id)
    if not donation:
        return jsonify(
            {
                "success": False,
                "error": "Donation not found"
            }
        ), 404

    db.session.delete(donation)
    db.session.commit()
    return jsonify(
        {
            "success": True,
            "message": "Donation successfully deleted"
        }
    ), 200


if __name__ == '__main__':
    app.run(debug=True)