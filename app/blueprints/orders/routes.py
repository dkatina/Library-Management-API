from flask import json, request, jsonify
from app.blueprints.orders import orders_bp
from app.blueprints.orders.schemas import order_schema, orders_schema, create_order_schema, receipt_schema
from marshmallow import ValidationError
from app.models import Order, OrderItems, db
from sqlalchemy import select
from datetime import date

@orders_bp.route("/", methods=["POST"])
def create_order():
    try:
        order_data = create_order_schema.load(request.json)
        print("PRINTING", order_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_order = Order(member_id=order_data['member_id'], order_date=date.today())

    db.session.add(new_order)
    db.session.commit()

    for item in order_data['item_quant']:
        order_item = OrderItems(order_id=new_order.id, item_id=item['item_id'], quantity=item['item_quant'])
        db.session.add(order_item)

    db.session.commit()

    total = 0
    for order_item in new_order.order_items:
        price = order_item.quantity * order_item.item.price
        total += price

    receipt ={
        "total": total,
        "order": new_order
    }

    return receipt_schema.jsonify(receipt), 201





