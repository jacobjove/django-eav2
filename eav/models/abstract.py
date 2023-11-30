from typing import Any, Generic, Self, TypeVar, override

from django.db.models import (
    CASCADE,
    PROTECT,
    ForeignKey,
    ManyToManyField,
    Model,
    UniqueConstraint,
)

from .attribute import Attribute

EntityT = TypeVar("EntityT", bound=Model)
KlassT = TypeVar(  # noqa: PLC0105
    "KlassT",
    bound="AbstractKlass[Any, Any]",
    covariant=True,
)
AttributeAssignmentT = TypeVar(  # noqa: PLC0105
    "AttributeAssignmentT",
    bound="Model",
    covariant=True,
)


class AttributesField(
    ManyToManyField,  # pyright: ignore[reportMissingTypeArgument]
    Generic[AttributeAssignmentT],
):
    @override
    def __new__(cls, **kwargs) -> "Self":
        return super().__new__(cls)  # type: ignore

    @override
    def __init__(self, *, through: None | type[AttributeAssignmentT] = None) -> None:
        super().__init__(to=Attribute, through=through)


class AbstractAttributeAssignment(Model):
    attribute = ForeignKey(Attribute, on_delete=PROTECT)
    attribute_id: int

    class Meta:
        abstract = True


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


class KlassAttributeAssignment(AbstractKlassAttributeAssignment["Klass"]):
    klass: "ForeignKey[Klass]" = ForeignKey("eav.Klass", on_delete=CASCADE)


class AbstractKlass(Model, Generic[EntityT, AttributeAssignmentT]):
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
            "AbstractKlass[EntityT, AttributeAssignmentT]",
        ]
    ]

    class Meta:
        abstract = True


class Klass(AbstractKlass[Any, KlassAttributeAssignment]):
    attributes = AttributesField(through=KlassAttributeAssignment)


class AbstractEntityAttributeAssignment(AbstractAttributeAssignment, Generic[EntityT]):
    # TODO: runtime check for implementation
    entity: "ForeignKey[EntityT]"
    assignment: "ForeignKey[AbstractKlassAttributeAssignment[Any]]"

    class Meta:
        abstract = True
        constraints = (
            UniqueConstraint(
                fields=["entity", "attribute"],
                name="unique_%(app_label)s_%(class)s_attribute",
            ),
        )

    @property
    def attribute(self):
        return self.assignment.attribute

    @property
    def attribute_pk(self):
        return self.assignment.attribute_id
