import httpx
import uvicorn
from uvicorn.protocols.http.flow_control import HIGH_WATER_LIMIT

print(f"{uvicorn.__version__=}")

small_payload = b"S" * HIGH_WATER_LIMIT
large_payload = b"L" * (HIGH_WATER_LIMIT + 1)

with httpx.Client(base_url="http://localhost:8000") as client:
    print("any previous request")
    for _ in range(2):
        client.post("/", content=small_payload).raise_for_status()
        print("-" * 80)

    print("sending large payload")
    client.post(
        "/",
        content=large_payload,
    ).raise_for_status()
    print("-" * 80)

    print("any subsequent request")
    for _ in range(2):
        client.post("/", content=small_payload).raise_for_status()
        print("-" * 80)
