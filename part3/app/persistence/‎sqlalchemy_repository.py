"""
SQLAlchemyRepository: implementation of the generic Repository interface
using SQLAlchemy for permanent persistence.
"""

from app import db
from app.persistence.repository import Repository

class SQLAlchemyRepository(Repository):
    """Generic repository that delegates CRUD operations to SQLAlchemy."""

    def __init__(self, model):
        self.model = model

    # -------- CRUD --------
    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    # -------- extra helpers --------
    def get_by_attribute(self, attr_name, attr_value):
        return (
            self.model.query.filter_by(**{attr_name: attr_value}).first()
        )
