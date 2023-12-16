from typing import TYPE_CHECKING, Any, Generic, TypeVar
from django.db.models import (
    PROTECT,
    ForeignKey,
    Model,
    UniqueConstraint,
)

if TYPE_CHECKING:
    from .entity_attribute_assignment import AbstractEntityAttributeAssignment
    from .klass_attribute_assignment import AbstractKlassAttributeAssignment
    from .klass import AbstractKlass
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
