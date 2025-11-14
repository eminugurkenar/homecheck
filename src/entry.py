import json
import time
from workers import Response, WorkerEntrypoint
from check import check


class Default(WorkerEntrypoint):
    async def scheduled(self, controller, env, ctx):
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

    async def fetch(self, request):
        stmt = """
            SELECT deviceId, timestamp, data
            FROM device_logs
            WHERE deviceId = ?
            ORDER BY timestamp DESC
            LIMIT 1
            """
        row = await self.env.DB.prepare(stmt).bind(self.env.TUYA_DEVICE_ID).first()
        if not row:
            return Response("No data found", status=404)

        return Response.json(row)
