import pytest
from unittest.mock import patch
from flask import json
from staff import app, Staff

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():
        with app.test_client() as client:
            yield client

def mock_to_dict(instance):
    return {
        "id": instance.id,
        "BLOOD_BANKS_id":instance.BLOOD_BANKS_id,
        "ADDRESS_id": instance.ADDRESS_id,
        "category": instance.category,
        "gender": instance.gender,
        "job_title": instance.job_title,
        "name": instance.name,
        "birthdate":instance.birthdate
        
    }
def test_get_staff(client):
    mock_staff = [
        type('MockStaff', (object,), {
            "id": 1,
            "BLOOD_BANKS_id":2,
            "ADDRESS_id": 4,
            "category": "Nurse",
            "gender": "Male",
            "job_title": "Blood Donation Nurse",
            "name": "Ricky Castillo",
            "birthdate":"2000-10-09",
            "to_dict": lambda self: mock_to_dict(self)
        })(),
        type('MockStaff', (object,), {
            "id": 2,
            "BLOOD_BANKS_id":4,
            "ADDRESS_id": 8,
            "category": "Manager",
            "gender": "Female",
            "job_title": "Quality Control Manager",
            "name": "Kae Airra Antonio",
            "birthdate":"2002-01-03",
            "to_dict": lambda self: mock_to_dict(self)
        })()
    ]

    with patch('staff.Staff.query.all', return_value=mock_staff):
        response = client.get("/staff")
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert json_data["success"] is True
        assert len(json_data["data"]) == 25
        assert json_data["data"][0]["name"] == "John Doe"

def test_get_single_staff(client):
    mock_staff = type('MockStaff', (object,), {
        "id": 1,
        "BLOOD_BANKS_id":2,
        "ADDRESS_id": 4,
        "category": "Nurse",
        "gender": "Male",
        "job_title": "Blood Donation Nurse",
        "name": "Ricky Castillo",
        "birthdate":"2000-10-09",
        "to_dict": lambda self: mock_to_dict(self)
    })()

    with patch('staff.db.session.get', return_value=mock_staff):
        response = client.get("/staff/1")
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert json_data["success"] is True
        assert json_data["data"]["id"] == 1
        assert json_data["data"]["name"] == "Ricky Castillo"

def test_update_staff(client):
    mock_staff = type('MockStaff', (object,), {
        "id": 1,
        "BLOOD_BANKS_id":2,
        "ADDRESS_id": 4,
        "category": "Nurse",
        "gender": "Male",
        "job_title": "Blood Donation Nurse",
        "name": "Ricky Castillo",
        "birthdate":"2000-10-09",
        "to_dict": lambda self: mock_to_dict(self)
    })()

    updated_data = {
        "BLOOD_BANKS_id":3,
        "ADDRESS_id": 5,
        "category": "Technician",
        "gender": "Updated Male",
        "job_title": "Lab Technician",
        "name": "Updated Ricky Castillo",
        "birthdate":"2000-10-10"
    }

    with patch('staff.db.session.get', return_value=mock_staff):
        response = client.put("/staff/1", 
                              data=json.dumps(updated_data), 
                              content_type='application/json')
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert json_data["success"] is True
        assert json_data["data"]["name"] == "Updated Ricky Castillo"

def test_delete_staff(client):
    mock_staff = Staff(
        id=1,
        BLOOD_BANKS_id=2,
        ADDRESS_id=4,
        category="Nurse",
        gender="Male",
        job_title="Blood Donation Nurse",
        name="Ricky Castillo",
        birthdate="2000-10-09"
    )

    with patch('staff.db.session.get', return_value=mock_staff):
        with patch('staff.db.session.delete') as mock_delete:
            response = client.delete("/staff/1")
            mock_delete.assert_called_once_with(mock_staff)
            assert response.status_code == 200
            json_data = json.loads(response.data)
            assert json_data["success"] is True
            assert "Staff successfully deleted" in json_data["message"]
