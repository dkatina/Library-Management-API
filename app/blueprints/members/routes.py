from flask import request, jsonify, session
from app.blueprints.members import members_bp
from app.blueprints.members.schemas import member_schema, members_schema, login_schema
from marshmallow import ValidationError
from app.models import Member, db
from sqlalchemy import select, delete
from app.extensions import limiter
from app.utils.util import encode_token, token_required


@members_bp.route("/login", methods=['POST'])
def login():

    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Member).where(Member.email == email)
    member = db.session.execute(query).scalars().first()

    if member and member.password == password:
        token = encode_token(member.id)

        response = {
            "status": "success",
            "message": "successfully logged in.",
            "token": token
        }

        return jsonify(response), 200
    else:
        return jsonify({"message": "Invalid email or password!"}), 400


@members_bp.route("/", methods=['POST'])
@limiter.limit("3 per hour")
def create_member():
    try: 
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(e.messages)
        return jsonify(e.messages), 400
    
    new_member = Member(name=member_data['name'], email=member_data['email'], DOB=member_data['DOB'], password=member_data['password'])
    
    db.session.add(new_member)
    db.session.commit()

    return member_schema.jsonify(new_member), 201


@members_bp.route("/", methods=['GET'])
def get_members():
    query = select(Member)
    result = db.session.execute(query).scalars().all()
    return members_schema.jsonify(result), 200


@members_bp.route("/", methods=["PUT"])
@token_required
def update_member(member_id):
    query = select(Member).where(Member.id == member_id)
    member = db.session.execute(query).scalars().first()
    
    if member == None:
        return jsonify({"message": "invalid member id"})
    
    try: 
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in member_data.items():
        setattr(member, field, value)

    db.session.commit()
    return member_schema.jsonify(member), 200

@members_bp.route("/", methods=['DELETE'])
@token_required
def delete_member(member_id):
    query = select(Member).where(Member.id == member_id)
    member = db.session.execute(query).scalars().first()

    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": f"succesfully deleted user {member_id}"})