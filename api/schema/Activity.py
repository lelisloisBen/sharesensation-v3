
from database import ma
from database.model.Activity import Activity


class ActivitySchema(ma.SQLAlchemyAutoSchema):
    """Make User object as serializable"""
    class Meta:
        model = Activity
