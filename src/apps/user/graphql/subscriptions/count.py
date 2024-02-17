import asyncio
from collections.abc import AsyncGenerator

import strawberry


@strawberry.type
class CountSubscription:
    @strawberry.subscription
    async def count(self, target: int = 100) -> AsyncGenerator[int, None]:
        for i in range(target):
            yield i
            await asyncio.sleep(0.5)
