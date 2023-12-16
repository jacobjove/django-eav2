from typing import TYPE_CHECKING, Any, Generic, Self, TypeVar, override

from django.db.models import ManyToManyField

from ..attribute import Attribute

if TYPE_CHECKING:
    from .klass_attribute_assignment import AbstractKlassAttributeAssignment


KlassAttributeAssignmentT = TypeVar(  # noqa: PLC0105
    "KlassAttributeAssignmentT",
    bound="AbstractKlassAttributeAssignment[Any]",
    covariant=True,
)


class AttributesField(
    ManyToManyField,  # pyright: ignore[reportMissingTypeArgument]
    Generic[KlassAttributeAssignmentT],
):
    @override
    def __new__(cls, **kwargs) -> "Self":
        return super().__new__(cls)  # type: ignore

    @override
    def __init__(
        self,
        through: None | type[KlassAttributeAssignmentT] = None,
        **kwargs,
    ) -> None:
        to = kwargs.pop("to", Attribute)
        super().__init__(to, through=through, **kwargs)


