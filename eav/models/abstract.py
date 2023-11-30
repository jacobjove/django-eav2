from typing import Any, Generic, Self, TypeVar, override

from abc import ABCMeta, abstractmethod

from django.db.models import (
    CASCADE,
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
KlassT = TypeVar("KlassT", bound="AbstractKlass[Any]")
AttributeAssignmentT = TypeVar("AttributeAssignmentT", bound="Model")


class AttributesField(
    ManyToManyField,  # pyright: ignore[reportMissingTypeArgument]
    Generic[AttributeAssignmentT],
):
    @override
    def __new__(cls, **kwargs) -> "ManyToManyField[Attribute, AttributeAssignmentT]":
        return super().__new__(cls)  # type: ignore

    @override
    def __init__(self, *, through: None | AttributeAssignmentT = None) -> None:
        super().__init__(to=Attribute, through=through)


class AbstractKlassAttributeAssignment(Model, Generic[KlassT, EntityT]):
    attribute = ForeignKey(Attribute, on_delete=PROTECT)

    class Meta:
        abstract = True
        constraints = UniqueConstraint(
            fields=["entity", "attribute"],
            name="unique_%(app_name)s_%(class)s_attribute",
        )

    @property
    @abstractmethod
    def klass(self) -> "ForeignKey[KlassT]":  # type: ignore
        """Must be defined by Klass models."""

    klass: KlassT


class KlassAttributeAssignment(AbstractKlassAttributeAssignment["Klass", Any]):
    klass: "ForeignKey[Klass]" = ForeignKey("eav.Klass", on_delete=CASCADE)


class AbstractKlass(AbstractBaseModel, Generic[EntityT]):
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
    def attributes(  # type: ignore
        self,
    ) -> AttributesField[AbstractKlassAttributeAssignment[type[Self], EntityT]]:
        """Must be defined by Klass models."""

    attributes: Any


class Klass(AbstractKlass[Any]):
    attributes = AttributesField(through=KlassAttributeAssignment)
