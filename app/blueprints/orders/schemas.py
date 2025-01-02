from app.models import Order, OrderItems
from app.extensions import ma
from marshmallow import fields


class ReceiptSchema(ma.Schema):
    '''
    total: 41.06
    order: {
            order_id: 1,
            member_id: 1,
            order_date: 2024-10-08,
            order_items: [
            {
                item:{item_name: "PSL", price:13.02},
                quantity: 3
            },
            {
                item:{item_name: "Scone", price:2.00},
                quantity: 1
            }
            ]
            }
    '''
    total = fields.Int(required=True)
    order = fields.Nested("OrderSchema")

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_relationships = True
    order_items = fields.Nested("OrderItemSchema",exclude=['id'], many=True)

class OrderItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItems
    item = fields.Nested("ItemSchema", exclude=["id"])


class CreateOrderSchema(ma.Schema):
    '''
    {
        member_id: 1
        item_quant: [{item_id: 1, item_quant: 3}]
    }
    '''
    member_id = fields.Int(required=True)
    item_quant = fields.Nested("ItemQuantSchema", many=True)

class ItemQuantSchema(ma.Schema):
    item_id = fields.Int(required=True)
    item_quant = fields.Int(required=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
create_order_schema = CreateOrderSchema()
receipt_schema = ReceiptSchema()
