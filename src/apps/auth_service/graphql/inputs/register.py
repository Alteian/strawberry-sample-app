import strawberry


@strawberry.input
class RegisterInput:
    first_name: str
    last_name: str
    email: str
    password: str
