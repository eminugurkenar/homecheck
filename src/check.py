import httpx
import json
from tuya import TuyaApi

async def check(TUYA_API_ENDPOINT: str, TUYA_ACCESS_ID: str, TUYA_ACCESS_KEY: str, TUYA_DEVICE_ID: str):
    tuya = TuyaApi(
        endpoint=TUYA_API_ENDPOINT,
        access_id=TUYA_ACCESS_ID,
        access_secret=TUYA_ACCESS_KEY)

    token = await tuya.get("", "/v1.0/token", {"grant_type": "1"})

    device = await tuya.get(token.json()['result']['access_token'], f"/v1.0/devices/{ TUYA_DEVICE_ID }")
    return device.json()
