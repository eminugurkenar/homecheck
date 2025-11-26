import json
import time
from urllib.parse import urlparse
from pathlib import Path
from workers import Response, WorkerEntrypoint
from check import check
from jinja2 import Environment, Template
from datetime import datetime, timezone, timedelta

class Default(WorkerEntrypoint):
    async def scheduled(self, controller, env, ctx):
        device_ids = [d.strip() for d in self.env.TUYA_DEVICE_IDS.split(",") if d.strip()]

        for device_id in device_ids:
            data = await check(
                self.env.TUYA_API_ENDPOINT,
                self.env.TUYA_ACCESS_ID,
                self.env.TUYA_ACCESS_KEY,
                device_id,
            )

            now = int(time.time() * 1000)
            stmt = """
                INSERT INTO device_logs (deviceId, timestamp, data)
                VALUES (?, ?, ?)
                """
            await (
                self.env.DB.prepare(stmt)
                .bind(device_id, now, json.dumps(data))
                .run()
            )

    async def fetch(self, request):
        status_code = 200
        url = urlparse(request.url)

        if url.path in ["/static/style.css"]:
            return await self.env.ASSETS.fetch(request)

        device_ids = [d.strip() for d in self.env.TUYA_DEVICE_IDS.split(",") if d.strip()]
        device_ids.append("ac180p")

        stmt = """
            SELECT deviceId, timestamp, data
            FROM device_logs
            WHERE deviceId = ?
            ORDER BY timestamp DESC
            LIMIT 1
            """

        devices = []

        for device_id in device_ids:
            row = await self.env.DB.prepare(stmt).bind(device_id).first()
            if not row:
                status_code = 404

                devices.append({
                    "device": {
                        "id": "not found",
                    },
                    "check": {
                        "time": None
                    },
                    "status": {},
                    "log": {}
                })
                continue

            devices.append({
                "device": {
                    "id": row.deviceId,
                },
                "check": {
                    "time": row.timestamp,
                },
                "status": json.loads(row.data)["status"]["result"],
                "log": json.loads(row.data)["log"]["result"]
            })

        html_file = Path(__file__).parent / "templates/index.html"

        env = Environment()
        env.filters['gmt3'] = gmt3_filter
        template = env.from_string(html_file.read_text())
        html = template.render(devices=devices)

        return Response(html, status=status_code, headers={"Content-Type": "text/html"} )


def gmt3_filter(timestamp):
    if timestamp is None:
        return ""

    if timestamp > 1e12:
        timestamp = timestamp / 1000

    dt = datetime.fromtimestamp(timestamp , tz=timezone.utc)
    dt = dt + timedelta(hours=3)
    return dt.strftime("%Y-%m-%d %H:%M:%S")