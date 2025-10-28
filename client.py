import httpx
from uvicorn.protocols.http.flow_control import HIGH_WATER_LIMIT

# A large payload to ensure it's sent in multiple chunks
large_payload = b'A' * (HIGH_WATER_LIMIT + 1)

with httpx.Client(base_url="http://localhost:8000") as client:
    client.post(
        "/large",
        content=large_payload,
        headers={"Content-Type": "application/octet-stream"}
    ).raise_for_status()

    client.get("/any").raise_for_status()
