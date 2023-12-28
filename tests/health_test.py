import pytest
from cloudevents.http import CloudEvent
from cloudevents.conversion import to_binary
from httpx import AsyncClient, _status_codes


@pytest.mark.asyncio
async def test_post_request():
    url = "http://localhost:5000/api/v1/health"
    attributes = {
        "Content-Type": "application/cloudevents+json",
        "specversion": "1.0",
        "type": "dev.knative.staging.helloworld-function",
        "source": "dev.knative.staging/localhost-dev",
        "subject": "helloworld",
        "time": "2018-04-05T17:31:00Z",
    }
    payload = None

    event = CloudEvent(attributes, payload)
    headers, data = to_binary(event)

    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, content=data)
        print(response.content)
        print(response.headers)

    assert response.status_code == _status_codes.codes.NO_CONTENT  # 204
