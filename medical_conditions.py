from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/bloodbank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class MedicalCondition(db.Model):
    __tablename__='medical_conditions'
    code = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    other_details = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "other_details": self.other_details
        }
    
@app.route("/medical_condition", methods=["GET"])
def get_all_medical_condition():
    medConn = MedicalCondition.query.all()
    return jsonify(
        {
            "success": True,
            "data": [medconn.to_dict() for medconn in medConn]
        }
    ), 200

@app.route("/medical_condition/<int:code>", methods=['GET'])
def get_single_medical_condition(code):
    medConn = db.session.get(MedicalCondition, code)
    if not medConn:
        return jsonify(
            {
                "success": False,
                "error": "Medical Condition not found"
            }
        ), 404
    return jsonify(
        {
            "success": True,
            "data": medConn.to_dict()
        }
    ), 200

@app.route("/medical_condition", methods=['POST'])
def add_medical_condition():
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

    required_fields = ["code", "name", "description", "other_details"]

    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing field: {field}"
                }
            ), 400

    try:
        new_medConn= MedicalCondition(
            code = data['code'],
            description = data['description'],
            other_details = data['other_details']

       )
        db.session.add(new_medConn)
        db.session.commit()
        return jsonify(
            {
                "success": True,
                "data": new_medConn.to_dict()
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
    
@app.route("/medical_condition/<int:code>", methods=["PUT"])
def update_medical_condition(code):
    medConn= db.session.get(MedicalCondition, code)
    if not medConn:
        return jsonify(
            {
                "success": False,
                "error": "Medical Condition not found"
            }
        ), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Invalid JSON"}), 400

    updatable_fields = ["code","description", "other_details"]
    for field in updatable_fields:
        if field in data:
            setattr(medConn, field, data[field])

    db.session.commit()
    return jsonify(
        {
            "success": True,
            "data": medConn.to_dict()
        }
    ), 200

@app.route("/medical_condition/<int:code>", methods=["DELETE"])
def delete_medical_condition(id):
    medConn = db.session.get(MedicalCondition, id)
    if not medConn:
        return jsonify(
            {
                "success": False,
                "error": "Medical Condition not found"
            }
        ), 404

    db.session.delete(medConn)
    db.session.commit()
    return jsonify(
        {
            "success": True,
            "message": "Medical Condition successfully deleted"
        }
    ), 200


if __name__ == '__main__':
    app.run(debug=True)