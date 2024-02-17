import strawberry
import strawberry_django

from src.apps.user.graphql.types import UserType
from src.apps.user.models import User


@strawberry_django.input(User, fields=["first_name", "last_name", "email", "password"])
class UserInput:
    pass


@strawberry_django.partial(User)
class UserInputPartial(strawberry_django.NodeInput):
    first_name: strawberry.auto
    last_name: strawberry.auto
    email: strawberry.auto
    password: strawberry.auto


@strawberry.type
class GenericMutation:
    create_user_generric: UserType = strawberry_django.mutations.create(UserInput)
    update_user_generic: UserType = strawberry_django.mutations.update(UserInputPartial)
    delete_user_generic: UserType = strawberry_django.mutations.delete(strawberry_django.NodeInput)
    create_users_in_bulk: list[UserType] = strawberry_django.mutations.create(UserInput)
