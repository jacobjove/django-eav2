from typing import Any, Generic, Self, TypeVar, override

from abc import ABCMeta, abstractmethod

from django.db.models import (
    PROTECT,
    ForeignKey,
    ManyToManyField,
    Model,
    UniqueConstraint,
)

from .attribute import Attribute


class AbstractModelMeta(ABCMeta, type(Model)):
    pass


class AbstractBaseModel(Model, metaclass=AbstractModelMeta):
    class Meta:
        abstract = True


EntityT = TypeVar("EntityT", bound=Model)
KlassT = TypeVar("KlassT", bound="Klass[Any]")
AttributeAssignmentT = TypeVar("AttributeAssignmentT", bound="Model")


class AttributesField(
    ManyToManyField[Attribute, AttributeAssignmentT],
    Generic[AttributeAssignmentT],
):
    @override
    def __init__(self, through: AttributeAssignmentT, **kwargs) -> None:
        super().__init__(through=through, **kwargs)


class KlassAttributeAssignment(Model, Generic[KlassT, EntityT]):
    attribute = ForeignKey(Attribute, on_delete=PROTECT)

    class Meta:
        abstract = True
        constraints = UniqueConstraint(
            fields=["entity", "attribute"],
            name="unique_%(app_name)s_%(class)s_attribute",
        )

    @property
    @abstractmethod
    def klass(
        self,
    ) -> "ForeignKey[KlassT]":
        """Must be defined by Klass models."""


class Klass(AbstractBaseModel, Generic[EntityT]):
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

    class Meta:
        abstract = True

    @property
    @abstractmethod
    def attributes(
        self,
    ) -> AttributesField[KlassAttributeAssignment[type[Self], EntityT]]:
        """Must be defined by Klass models."""
