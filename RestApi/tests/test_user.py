from models import Session, User
from run_app import app
import pytest
import bcrypt
import json


session = Session()
app_context = app.app_context()
app_context.push()
client = app.test_client()


URL = '/user/'

user = {
    "username": "olga",
    "email": "olga@gmail.com",
    "password": "1-1-1-1",
    "register_date": "2022-5-27 12:00:00"
}

new_user = {
    "username": "new-username",
    "email": "new-email@gmail.com",
    "password": "0-0-0-0",
    "register_date": "2022-5-27 12:00:00"
}

new_fields = {
    "username": "new-username-field",
    "password": "new-password-field"
}

@pytest.fixture
def dbUser():
    user = User(username="maks",
                email="mask@gmail.com",
                password=bcrypt.hashpw("121212".encode("utf-8"), bcrypt.gensalt()),
                register_date="2022-5-27 12:00:00")
    Session.add(user)
    Session.commit()
    yield
    user = Session.query(User).filter_by(username="maks").first()
    Session.delete(user)
    Session.commit()


def test_post_delete():
    response_create = client.post(URL, data=json.dumps(user))
    assert response_create.status_code == 200
    response_delete = client.delete(URL + str(response_create.json["id"]) + "/")
    assert response_delete.status_code == 200
    response_delete_nf = client.delete(URL + str(1000) + "/")
    assert response_delete_nf.status_code == 404

def test_get_1(dbUser):
    response_get = client.get(URL)
    assert response_get.status_code == 200

def test_get_2():
    response_create = client.post(URL, data=json.dumps(user))
    response_get_id = client.get(URL + str(response_create.json["id"]) + "/")
    assert response_get_id.status_code == 200
    response_get_id_nf = client.get(URL + str(1000) + "/")
    assert response_get_id_nf.status_code == 404
    client.delete(URL + str(response_create.json["id"]) + "/")

def test_put():
    response_create = client.post(URL, data=json.dumps(user))
    response_update = client.put(URL + str(response_create.json["id"]) + "/", data=json.dumps(new_user))
    assert response_update.status_code == 200
    assert response_update.json["username"] == "new-username"
    response_update_nf = client.put(URL + str(1000) + "/", data=json.dumps(new_user))
    assert response_update_nf.status_code == 404
    client.delete(URL + str(response_create.json["id"]) + "/")

def test_patch():
    response_create = client.post(URL, data=json.dumps(user))
    response_patch = client.patch(URL + str(response_create.json["id"]) + "/", data=json.dumps(new_fields))
    assert response_patch.status_code == 200
    assert response_patch.json["username"] == "new-username-field"
    response_patch_nf = client.patch(URL + str(1000) + "/", data=json.dumps(new_fields))
    assert response_patch_nf.status_code == 404
    client.delete(URL + str(response_create.json["id"]) + "/")