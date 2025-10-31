# asyncio-contextvars-pollution

Building a minimal example for [Kludex/uvicorn#2167](https://github.com/Kludex/uvicorn/issues/2167) to determine whether this is on `asyncio` as suggested in the issue or `uvicorn`.

## Reproduce

- `app.py` contains a minimal ASGI application, which
  - saves the context for the incoming request,
  - sets a request ID in the context,
  - saves the context again,
  - prints the context in its before and after state, and
  - responds with a 200 status code and an empty body.
- `client.py`
  - prints the `uvicorn` version
  - sends two small (64kB) POST requests
  - sends one large (> 64kB) POST request
  - sends to small (64kB) POST requests

  to the server

### Broken (`--loop asyncio`)

```bash
$ uv run uvicorn --no-access-log --loop asyncio app:app 2> /dev/null & SERVER_PID=$! && \
  sleep 3 && \
  uv run python client.py && \
  kill $SERVER_PID
uvicorn.__version__='0.38.0'
any previous request
{'before': {}, 'after': {'id': '4050d765-d593-4e4c-869c-d7a14fa3afad'}}
--------------------------------------------------------------------------------
{'before': {}, 'after': {'id': 'c366235d-3e35-42c3-96a7-011857ee5327'}}
--------------------------------------------------------------------------------
sending large payload
{'before': {}, 'after': {'id': '33d2e3bb-b169-4dd6-a13e-087cde9e31b9'}}
--------------------------------------------------------------------------------
any subsequent request
{'before': {'id': '33d2e3bb-b169-4dd6-a13e-087cde9e31b9'},
 'after': {'id': '1adaa475-9a97-48c3-a45a-cc2ee4b280a0'}}
--------------------------------------------------------------------------------
{'before': {'id': '33d2e3bb-b169-4dd6-a13e-087cde9e31b9'},
 'after': {'id': '20763cdc-26a7-4d98-bfbc-182ac561fdf6'}}
--------------------------------------------------------------------------------
```

### Functional (`--loop uvloop`)

```bash
$ uv run uvicorn --no-access-log --loop uvloop app:app 2> /dev/null & SERVER_PID=$! && \
  sleep 3 && \
  uv run python client.py && \
  kill $SERVER_PID
uvicorn.__version__='0.38.0'
any previous request
{'before': {}, 'after': {'id': '5389ded1-bf67-4f29-9105-97ebbc053cef'}}
--------------------------------------------------------------------------------
{'before': {}, 'after': {'id': '7ebb5322-58e4-4562-9945-de1968362af5'}}
--------------------------------------------------------------------------------
sending large payload
{'before': {}, 'after': {'id': '0576a478-cb1b-4da4-bf9a-462a82b550f6'}}
--------------------------------------------------------------------------------
any subsequent request
{'before': {}, 'after': {'id': '3c06493c-73ed-4fb0-8f7c-7044cbb056bf'}}
--------------------------------------------------------------------------------
{'before': {}, 'after': {'id': '15bba23f-a960-453b-911c-fcc4bf22c5ae'}}
--------------------------------------------------------------------------------
```
