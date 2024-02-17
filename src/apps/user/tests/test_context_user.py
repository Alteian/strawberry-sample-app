from typing import Any

import pytest
from strawberry_django.test.client import AsyncTestClient, Response


@pytest.mark.asyncio
async def test_anonymous_context_user(db: Any) -> None:
    client = AsyncTestClient("/graphql/")
    res = await client.query(
        """
        query context_user {
            contextUser {
                ... on ContextUserSuccess {
                    __typename
                    user {
                      email
                      firstName
                      id
                      isActive
                      isVerified
                      lastName
                      role
                    }
                }
                ... on ContextUserError {
                __typename
                message
                }
            }
        }
        """,
    )
    expected = Response(
        errors=None,
        data={"contextUser": {"__typename": "ContextUserError", "message": "User is not authenticated"}},
        extensions=None,
    )
    assert res == expected  # nosec: B101
