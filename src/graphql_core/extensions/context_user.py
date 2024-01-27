from functools import cached_property
from typing import Any, ClassVar, Optional

from strawberry import schema_directive
from strawberry.extensions.field_extension import (
    FieldExtension,
    SyncExtensionResolver,
)
from strawberry.field import StrawberryField
from strawberry.schema_directive import Location
from strawberry.types import Info


class ContextUserExtension(FieldExtension):
    SCHEMA_DIRECTIVE_LOCATIONS: ClassVar[list[Location]] = [Location.FIELD_DEFINITION]
    SCHEMA_DIRECTIVE_DESCRIPTION: ClassVar[Optional[str]] = "Used to trigger context user"

    def __init__(
        self,
        *,
        use_directives: bool = True,
    ):
        super().__init__()
        self.use_directives = use_directives

    def apply(self, field: StrawberryField) -> None:  # pragma: no cover
        if self.use_directives:
            field.directives.append(self.schema_directive)

    @cached_property
    def schema_directive(self) -> object:
        key = "__strawberry_directive_type__"
        directive_class = getattr(self.__class__, key, None)

        if directive_class is None:

            @schema_directive(
                name=self.__class__.__name__,
                locations=self.SCHEMA_DIRECTIVE_LOCATIONS,
                description=self.SCHEMA_DIRECTIVE_DESCRIPTION,
                repeatable=True,
            )
            class AutoDirective:
                ...

            directive_class = AutoDirective

        return directive_class()

    def resolve(self, next_: SyncExtensionResolver, source: Any, info: Info, **kwargs: Any) -> Any:
        assert info.context.user  # nosec: B101
        return next_(source, info, **kwargs)
