from django.db.models import (
    PROTECT,
    ForeignKey,
    Model,
)

from ..attribute import Attribute


class AbstractAttributeAssignment(Model):
    attribute = ForeignKey(Attribute, on_delete=PROTECT)
    attribute_id: int

    class Meta:
        abstract = True
