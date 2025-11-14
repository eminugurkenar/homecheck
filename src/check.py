import httpx
import json
import time
from tuya import TuyaApi


async def check(
    TUYA_API_ENDPOINT: str,
    TUYA_ACCESS_ID: str,
    TUYA_ACCESS_KEY: str,
    TUYA_DEVICE_ID: str,
):
    tuya = TuyaApi(
        endpoint=TUYA_API_ENDPOINT,
        access_id=TUYA_ACCESS_ID,
        access_secret=TUYA_ACCESS_KEY,
    )

    token = await tuya.get("", "/v1.0/token", {"grant_type": "1"})

    device_status = await tuya.get(
        token.json()["result"]["access_token"], f"/v1.0/devices/{TUYA_DEVICE_ID}"
    )

    now = int(time.time() * 1000)
    five_days = 5 * 24 * 60 * 60 * 1000
    start_ms = now - five_days
    end_ms = now

    device_logs = await tuya.get(
        token.json()["result"]["access_token"],
        f"/v2.0/cloud/thing/{TUYA_DEVICE_ID}/report-logs",
        {
            "codes": "watersensor_state,battery_percentage",
            "start_time": start_ms,
            "end_time": end_ms,
            "size": 50,
        },
    )
    return {"status": device_status.json(), "log": device_logs.json()}
