import pytest
from unittest.mock import patch
from flask import json
from donors import app, Donors

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():
        with app.test_client() as client:
            yield client

def mock_to_dict(instance):
    return {
        "id": instance.id,
        "gender": instance.gender,
        "birthdate": instance.birthdate,
        "name": instance.name,
        "contact": instance.contact,
        "BLOOD_BANKS_id": instance.BLOOD_BANKS_id,
        "MEDICATIONS_code": instance.MEDICATIONS_code,
        "MEDICAL_CONDITIONS_code": instance.MEDICAL_CONDITIONS_code
    }
def test_get_donors(client):
    mock_donors = [
        type('MockDonor', (object,), {
            "id": 1,
            "gender": "Male",
            "birthdate": "2000-10-09",
            "name": "John Doe",
            "contact": "09519872233",
            "BLOOD_BANKS_id": 18,
            "MEDICATIONS_code": 8,
            "MEDICAL_CONDITIONS_code": 1,
            "to_dict": lambda self: mock_to_dict(self)
        })(),
        type('MockDonor', (object,), {
            "id": 2,
            "gender": "Female",
            "birthdate": "2002-01-03",
            "name": "Kae Airra Antonio",
            "contact": "091234576",
            "BLOOD_BANKS_id": 12,
            "MEDICATIONS_code": 7,
            "MEDICAL_CONDITIONS_code": 10,
            "to_dict": lambda self: mock_to_dict(self)
        })()
    ]

    with patch('donors.Donors.query.all', return_value=mock_donors):
        response = client.get("/donor")
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert json_data["success"] is True
        assert len(json_data["data"]) == 25
        assert json_data["data"][0]["name"] == "John Doe"

def test_get_single_donor(client):
    mock_donor = type('MockDonor', (object,), {
        "id": 1,
        "gender": "Male",
        "birthdate": "2000-10-09",
        "name": "Ricky Castillo",
        "contact": "09519872233",
        "BLOOD_BANKS_id": 18,
        "MEDICATIONS_code": 8,
        "MEDICAL_CONDITIONS_code": 1,
        "to_dict": lambda self: mock_to_dict(self)
    })()

    with patch('donors.db.session.get', return_value=mock_donor):
        response = client.get("/donor/1")
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert json_data["success"] is True
        assert json_data["data"]["id"] == 1
        assert json_data["data"]["name"] == "Ricky Castillo"

def test_update_donor(client):
    mock_donor = type('MockDonor', (object,), {
        "id": 1,
        "gender": "Male",
        "birthdate": "2000-10-09",
        "name": "Ricky Castillo",
        "contact": "09519872233",
        "BLOOD_BANKS_id": 18,
        "MEDICATIONS_code": 8,
        "MEDICAL_CONDITIONS_code": 1,
        "to_dict": lambda self: mock_to_dict(self)
    })()

    updated_data = {
        "name": "Updated Ricky Castillo",
        "gender": "Female",
        "birthdate": "2000-10-09",
        "contact": "09519872233",
        "BLOOD_BANKS_id": 18,
        "MEDICATIONS_code": 8,
        "MEDICAL_CONDITIONS_code": 1
    }

    with patch('donors.db.session.get', return_value=mock_donor):
        response = client.put("/donor/1", 
                              data=json.dumps(updated_data), 
                              content_type='application/json')
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert json_data["success"] is True
        assert json_data["data"]["name"] == "Updated Ricky Castillo"

def test_delete_donor(client):
    mock_donor = Donors(
        id=1,
        gender="Male",
        birthdate="2000-10-09",
        name="Ricky Castillo",
        contact="09519872233",
        BLOOD_BANKS_id=18,
        MEDICATIONS_code=8,
        MEDICAL_CONDITIONS_code=1
    )

    with patch('donors.db.session.get', return_value=mock_donor):
        with patch('donors.db.session.delete') as mock_delete:
            response = client.delete("/donor/1")
            mock_delete.assert_called_once_with(mock_donor)
            assert response.status_code == 200
            json_data = json.loads(response.data)
            assert json_data["success"] is True
            assert "Donor successfully deleted" in json_data["message"]
