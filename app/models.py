import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    eid = db.Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    eid = db.Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    created_by = db.mapped_column(db.ForeignKey('users.eid'))
    active = db.Column(db.Boolean, default=True)

    @property
    def serialized(self):
        return {
            'eid': self.eid,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'created_by': self.created_by
        }