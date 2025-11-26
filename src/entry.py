import json
import time
from urllib.parse import urlparse
from pathlib import Path
from workers import Response, WorkerEntrypoint
from check import check
from jinja2 import Template



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
        url = urlparse(request.url)

        if url.path in ["/static/style.css"]:
            return await self.env.ASSETS.fetch(request)

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

        data = {
            "device": {
                "id": row.deviceId,
            },
            "check": {
                "time": row.timestamp,
            },
            "status": json.loads(row.data)["status"]["result"],
            "log": json.loads(row.data)["log"]["result"]
        }

        html_file = Path(__file__).parent / "templates/index.html"

        template = Template(html_file.read_text())
        html = template.render(check=data["check"],status=data["status"],log=data["log"])

        return Response(html, headers={"Content-Type": "text/html"})