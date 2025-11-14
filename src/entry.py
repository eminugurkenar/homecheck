import json
import time
from workers import Response, WorkerEntrypoint
from check import check


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        data = await check(
            self.env.TUYA_API_ENDPOINT,
            self.env.TUYA_ACCESS_ID,
            self.env.TUYA_ACCESS_KEY,
            self.env.TUYA_DEVICE_ID,
        )

        now = int(time.time() * 1000)
        stmt = """
            INSERT INTO device_logs (deviceId, timestamp, data)
            VALUES (?, ?, ?)
            """
        await (
            self.env.DB.prepare(stmt)
            .bind(self.env.TUYA_DEVICE_ID, now, json.dumps(data))
            .run()
        )

        return Response(json.dumps(data))
