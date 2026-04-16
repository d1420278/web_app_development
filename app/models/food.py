from datetime import datetime, timezone
from app.models import db

class Food(db.Model):
    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    portion = db.Column(db.Integer, nullable=False)
    original_price = db.Column(db.Integer, nullable=True)
    discount_price = db.Column(db.Integer, nullable=True)
    image_path = db.Column(db.String(255), nullable=True)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='available', nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship to explicit orders is attached to model directly
    orders = db.relationship('Order', backref='food', lazy=True)

    @classmethod
    def create(cls, **kwargs):
        new_food = cls(**kwargs)
        db.session.add(new_food)
        db.session.commit()
        return new_food

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, food_id):
        return db.session.get(cls, food_id)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
