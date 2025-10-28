# asyncio-contextvars-pollution

Building a minimal example for [Kludex/uvicorn#2167](https://github.com/Kludex/uvicorn/issues/2167) to determine whether this is on `asyncio` as suggested in the issue or `uvicorn`.

## Reproduce

- `app.py` contains a FastAPI ASGI application. It is instrumented with OpenTelemetry, which sets a trace ID for every incoming request.
- `client.py` sends a large enough HTTP request to the /large endpoint that triggers `uvicorn` to chunk the message. Afterward, it sends a small request to the /any endpoint.
- Both endpoints print the trace ID
- If everything is working correctly, each request should get their own trace ID as they are independent

### Broken

```bash
$ uv run uvicorn --loop asyncio app:app 2>&1 | grep reproduce &
[...]
$ uv run python client.py
```

### Functional

```bash
$ uv run uvicorn --loop uvloop app:app 2>&1 | grep reproduce &
[...]
$ uv run python client.py
```
