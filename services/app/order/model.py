from .. import db


class ItemsInOrder(db.Model):
    __tablename__ = "items_in_order"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column("item_id", db.Integer, db.ForeignKey("items.id"))
    order_id = db.Column("order_id", db.Integer, db.ForeignKey("orders.id"))
    quantity = db.Column(db.Integer)

    item = db.relationship("Item")
    order = db.relationship("OrderModel", back_populates="items")


class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    items = db.relationship("ItemsInOrder", back_populates="order", lazy='dynamic')


    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()
    
    @property
    def description(self):
        counts= [f'{data.quantity}x {data.item.name}' for data in self.items]
        return ",".join(counts)
    
    @property
    def amount(self):
        total = int(sum([item_data.item.price * item_data.quantity for item_data in self.items]))
        return total
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
