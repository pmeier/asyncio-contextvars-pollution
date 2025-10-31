import contextvars
import uuid
from pprint import pprint
from typing import Callable, Any, Awaitable

id_var = contextvars.ContextVar("id", default="")


async def app(
    scope: dict[str, Any],
    receive: Callable[[], Awaitable[dict[str, Any]]],
    send: Callable[[dict[str, Any]], Awaitable[None]],
) -> None:
    if scope["type"] != "http":
        return

    before = extract_contextvars()
    id_var.set(str(uuid.uuid4()))
    after = extract_contextvars()

    pprint({"before": before, "after": after}, sort_dicts=False)

    await handle_http(scope, receive, send)


def extract_contextvars() -> dict[str, Any]:
    return {c.name: v for c, v in contextvars.copy_context().items()}


async def handle_http(
    scope: dict[str, Any],
    receive: Callable[[], Awaitable[dict[str, Any]]],
    send: Callable[[dict[str, Any]], Awaitable[None]],
) -> None:
    while True:
        message = await receive()
        if message["type"] == "http.disconnect":
            return
        if not message["more_body"]:
            break

    await send(
        {
            "type": "http.response.start",
            "status": 200,
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": b"",
            "more_body": False,
        }
    )
