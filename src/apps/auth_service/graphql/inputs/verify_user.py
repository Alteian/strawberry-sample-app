import strawberry


@strawberry.input
class VerifyUserInput:
    verification_token: str
