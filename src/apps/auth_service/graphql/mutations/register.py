import strawberry
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _
from strawberry.types import Info

from src.apps.auth_service.graphql.exceptions import UserAlreadyExistsException
from src.apps.auth_service.graphql.inputs import RegisterInput
from src.apps.auth_service.graphql.payloads import RegisterError, RegisterPayload, RegisterSuccess


@strawberry.type
class RegisterMutation:
    @strawberry.mutation
    @sync_to_async
    def register(self, info: Info, input: RegisterInput) -> RegisterPayload:
        try:
            if get_user_model().objects.filter(email__iexact=input.email).exists():
                raise UserAlreadyExistsException
            get_user_model().objects.create_user(**vars(input))
            return RegisterSuccess(message=str(_("Verification e-mail has been sent, please check your inbox")))
        except IntegrityError:
            return RegisterError(message=str(_("User creation failed, please contact support")))
        except TypeError:
            return RegisterError(message=str(_("Invalid input")))
        except UserAlreadyExistsException:
            return RegisterError(message=str(_("User already exists")))
        except Exception as error:
            return RegisterError(message=str(error))
