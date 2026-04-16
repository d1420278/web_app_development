from datetime import datetime, timezone
from app.models import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='reserved', nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime, nullable=True)

    @classmethod
    def create(cls, **kwargs):
        new_order = cls(**kwargs)
        db.session.add(new_order)
        db.session.commit()
        return new_order

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, order_id):
        return db.session.get(cls, order_id)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        
    def complete_order(self):
        self.status = 'completed'
        self.completed_at = datetime.now(timezone.utc)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
