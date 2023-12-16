from typing import TYPE_CHECKING, Any, Generic, Self, TypeVar, override

from django.db.models import (
    PROTECT,
    ForeignKey,
    Model,
    UniqueConstraint,
)

from .attributes_field import AttributesField
from ..attribute import Attribute
from .attribute_assignment import AbstractAttributeAssignment

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager

    from ..value import Value


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
EntityAttributeAssignmentT = TypeVar(  # noqa: PLC0105
    "EntityAttributeAssignmentT",
    bound="AbstractEntityAttributeAssignment[Any, Any]",
    covariant=True,
)



class AbstractKlassAttributeAssignment(AbstractAttributeAssignment, Generic[KlassT]):
    # TODO: runtime check for implementation
    klass: "ForeignKey[KlassT]"

    class Meta:
        abstract = True
        constraints = (
            UniqueConstraint(
                fields=["klass", "attribute"],
                name="unique_%(app_label)s_%(class)s_attribute",
            ),
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


class AbstractEntityAttributeAssignment(
    Model,
    Generic[EntityT, KlassAttributeAssignmentT],
):
    # TODO: runtime check for implementation
    entity: "ForeignKey[EntityT]"
    entity_id: int

    # TODO: runtime check for implementation
    klass_attribute_assignment: "ForeignKey[KlassAttributeAssignmentT]"
    klass_attribute_assignment_id: int

    class Meta:
        abstract = True
        constraints = (
            UniqueConstraint(
                fields=["entity", "klass_attribute_assignment"],
                name="unique_%(app_label)s_%(class)s_klass_attribute_assignment",
            ),
        )

    @property
    def attribute(self) -> "Attribute":
        return self.klass_attribute_assignment.attribute

    @property
    def attribute_pk(self) -> int | str:
        return self.klass_attribute_assignment.attribute_id


class AbstractValueAssignment(Model, Generic[EntityAttributeAssignmentT]):
    value: "ForeignKey[Value]" = ForeignKey("eav.Value", on_delete=PROTECT)

    # TODO: add runtime check for implementation
    assignment: "ForeignKey[EntityAttributeAssignmentT]"

    class Meta:
        abstract = True
        constraints = (
            UniqueConstraint(
                fields=["value", "assignment"],
                name="unique_%(app_label)s_%(class)s_value_assignment",
            ),
        )
