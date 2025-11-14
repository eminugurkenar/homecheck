import json
from workers import Response, WorkerEntrypoint
from check import check


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        response = await check(
            self.env.TUYA_API_ENDPOINT,
            self.env.TUYA_ACCESS_ID,
            self.env.TUYA_ACCESS_KEY,
            self.env.TUYA_DEVICE_ID,
        )
        return Response(json.dumps(response))
