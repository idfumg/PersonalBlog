from app import db
from sqlalchemy.sql import func

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(64), nullable=False)
    intro = db.Column(db.String(254), nullable=False)
    text = db.Column(db.String, nullable=False)
    deleted = db.Column(db.Boolean, nullable=False, default=False)
    domain = db.Column(db.String(24), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return '<Post %r>' % self.header
