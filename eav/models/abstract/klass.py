from .attributes_field import AttributesField
from typing import TYPE_CHECKING, Any, Generic, TypeVar
from .klass_attribute_assignment import AbstractKlassAttributeAssignment
from django.db.models import (
    Model,
)


if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager


EntityT = TypeVar("EntityT", bound=Model)
KlassT = TypeVar(  # noqa: PLC0105
    "KlassT",
    bound="AbstractKlass[Any, Any]",
    covariant=True,
)
KlassAttributeAssignmentT = TypeVar(  # noqa: PLC0105
    "KlassAttributeAssignmentT",
    bound="AbstractKlassAttributeAssignment[Any]",
    covariant=True,
)



class AbstractKlass(Model, Generic[EntityT, KlassAttributeAssignmentT]):
    """
    Abstract model defining a relationship with a set of attributes.

    Example usage:
    ```
    from django.db.models import Model, ForeignKey
    from eav.models import AttributeContainer, AttributesField, KlassAttributeAssignment

    class ProductKlassAttributeAssignment(KlassAttributeAssignment["ProductKlass", "Product"]):
        pass

    class ProductKlass(Klass["Product"]):
        attributes = AttributesField(through=ProductKlassAttributeAssignment)

    class Product(Model):
        klass = ForeignKey(ProductClass)
    ```
    """

    # TODO: runtime check for implementation
    attributes: AttributesField[
        AbstractKlassAttributeAssignment[
            "AbstractKlass[EntityT, KlassAttributeAssignmentT]",
        ]
    ]
    attribute_assignments: "RelatedManager[AbstractKlassAttributeAssignment[AbstractKlass[EntityT, KlassAttributeAssignmentT]]]"

    class Meta:
        abstract = True
