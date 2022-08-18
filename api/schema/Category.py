
from database import ma
from database.model.Category import Category


class CategorySchema(ma.SQLAlchemyAutoSchema):
    """Make User object as serializable"""
    class Meta:
        model = Category
