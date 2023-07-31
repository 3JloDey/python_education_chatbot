import json

import httpx


class HastebinAPI:
    def __init__(self, token):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "text/plain",
        }

    async def create_document(self, data: str) -> str | None:
        async with httpx.AsyncClient(timeout=httpx.Timeout(15.0)) as ahtx:
            response = await ahtx.post(
                url="https://hastebin.com/documents", headers=self.headers, data=data
            )
            key = json.loads(response.text).get("key")
            if key is not None:
                return f"https://hastebin.com/share/{key}"
