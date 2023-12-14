"""
Spec Reference: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md
"""

import json
import unittest
from cloudevents.http import CloudEvent
from cloudevents.conversion import to_binary
from httpx import AsyncClient

attributes = {
    "type": "apigateway.interceptor",
    "producer": "apigateway.interceptor",
    "source": "telegram_server",
    "protocol": "http",
}
data = {
    "update_id": 323636054,
    "message": {
        "message_id": 17,
        "from": {
            "id": 1043656153,
            "is_bot": False,
            "first_name": "Kev",
            "username": "suggarrdaddy",
        },
        "chat": {
            "id": -933506457,
            "title": "dev",
            "type": "group",
            "all_members_are_administrators": True,
        },
        "date": 1702107527,
        "text": "hiiiii",
    },
}


class TestWebhook(unittest.IsolatedAsyncioTestCase):
    async def test_webhook(self):
        async with AsyncClient() as client:
            # Create a CloudEvent
            event = CloudEvent(attributes, data)

            # Creates the HTTP request representation of the CloudEvent in binary content mode
            headers, body = to_binary(event)

            # Make a POST request to the mock server
            response = await client.post(
                url="http://localhost:5000/api/v1/webhook",
                json=json.loads(body),
                headers=headers,
            )

            # Assert the response status code and content
            self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
