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
            "BLOOD_BANKS_id": self.BLOOD_BANKS_id,
            "ADDRESS_id": self.ADDRESS_id,
            "category": self.category,
            "gender": self.gender,
            "job_title": self.job_title,
            "name": self.name,
            "birthdate": self.birthdate
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