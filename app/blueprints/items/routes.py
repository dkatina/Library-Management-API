from flask import request, jsonify
from app.blueprints.items import items_bp
from app.blueprints.items.schemas import item_schema, items_schema
from marshmallow import ValidationError
from app.models import Item, db
from sqlalchemy import select



@items_bp.route("/", methods=['POST'])
def create_item():
    try: 
        item_data = item_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_item = Item(item_name=item_data['item_name'], price=item_data['price'])
    
    db.session.add(new_item)
    db.session.commit()

    return item_schema.jsonify(new_item), 201


@items_bp.route("/", methods=['GET'])
def get_items():
    query = select(Item)
    result = db.session.execute(query).scalars().all()
    return items_schema.jsonify(result), 200


@items_bp.route("/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    query = select(Item).where(Item.id == item_id)
    item = db.session.execute(query).scalars().first()
    
    if item == None:
        return jsonify({"message": "invalid item id"})
    
    try: 
        item_data = item_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in item_data.items():
        setattr(item, field, value)

    db.session.commit()
    return item_schema.jsonify(item), 200

@items_bp.route("/<int:item_id>", methods=['DELETE'])
def delete_item(item_id):
    query = select(Item).where(Item.id == item_id)
    item = db.session.execute(query).scalars().first()

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": f"succesfully deleted item {item_id}"})