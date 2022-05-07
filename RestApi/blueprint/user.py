from models import Session
from flask import jsonify, request, Response, Blueprint
from marshmallow import ValidationError
from models import User
from schemas import UserSchema
import bcrypt


user = Blueprint("user", __name__)


def is_short_password(string):
    return len(string) < 6


def is_simple_password(string):
    flag = True
    for i in range(len(string)):
        for j in range(len(string) - i):
            if string[i] != string[j]:
                flag = False
    return flag


@user.route("/user/", methods=["POST"])
def create_user():
    data = request.get_json(force=True)

    if is_short_password(request.json.get('password', None)) and is_simple_password(request.json.get('password', None)):
        return "[THIS PASSWORD IS NOT CORRECT]", 400
    
    try:
        UserSchema().load(data)
    except ValidationError:
        return "[THIS IS A VALIDATION ERROR]", 400

    password = request.json.get('password', None)
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    data.update({"password": hashed_password})

    entry = User(**data)
    Session.add(entry)
    Session.commit()

    return jsonify(UserSchema().dump(entry))


@user.route("/user/", methods=["GET"])
def get_all_users():
    entries = Session.query(User).all()
    return jsonify(UserSchema(many=True).dump(entries))


@user.route("/user/<int:id>/", methods=["GET"])
def get_user_by_id(id):
    entry = Session.query(User).filter_by(id=id).first()
    if entry is None:
        return Response(status=404, response="[SUCH USER ID DOES NOT EXIST]")
    return jsonify(UserSchema().dump(entry))


@user.route("/user/<int:id>/", methods=["PUT"])
def update_user_by_id(id):
    entry = Session.query(User).filter_by(id=id).first()
    if entry is None:
        return Response(status=404, response="[SUCH USER ID DOES NOT EXIST]\n[YOU CAN'T UPDATE HIM]")

    data = request.get_json(force=True)

    if is_short_password(request.json.get('password', None)) and is_simple_password(request.json.get('password', None)):
        return "[THIS PASSWORD IS NOT CORRECT]", 400
    
    try:
        UserSchema().load(data)
    except ValidationError:
        return "[THIS IS A VALIDATION ERROR]", 400
    
    password = request.json.get('password', None)
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    data.update({"password": hashed_password})

    for key, value in data.items():
        setattr(entry, key, value)
    
    Session.add(entry)
    Session.commit()
    
    return jsonify(UserSchema().dump(entry))


@user.route("/user/<int:id>/", methods=["PATCH"])
async def patch_user_by_id(id):
    entry = Session.query(User).filter_by(id=id).first()
    if entry is None:
        return Response(status=404, response="[SUCH USER ID DOES NOT EXIST]\n[YOU CAN'T PATCH HIM]")

    data = request.get_json(force=True)

    try:
        UserSchema().load(data)
    except ValidationError:
        return "[THIS IS A VALIDATION ERROR]", 400
    
    if request.json.get('password') != None:
        if is_short_password(request.json.get('password', None)) and is_simple_password(request.json.get('password', None)):
            return "[THIS PASSWORD IS NOT CORRECT]", 400
        hashed_password = bcrypt.hashpw(request.json.get('password').encode("utf-8"), bcrypt.gensalt())
        data.update({"password": hashed_password})

    for key, value in data.items():
        setattr(entry, key, value)
    
    Session.add(entry)
    Session.commit()
    
    return jsonify(UserSchema().dump(entry))


@user.route("/user/<string:id>/", methods=["DELETE"])
def delete_user_by_id(id):
    entry = Session.query(User).filter_by(id=id).first()
    if entry is None:
        return Response(status=404, response="[SUCH USER ID DOES NOT EXIST]")
    Session.delete(entry)
    Session.commit()
    return jsonify(UserSchema().dump(entry))