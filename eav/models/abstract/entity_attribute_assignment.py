from typing import Any, Generic, TypeVar

from django.db.models import (
    ForeignKey,
    Model,
    UniqueConstraint,
)

from .klass import AbstractKlass
from .klass_attribute_assignment import AbstractKlassAttributeAssignment
from ..attribute import Attribute


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
