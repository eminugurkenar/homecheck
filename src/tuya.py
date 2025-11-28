import httpx
import time
import hashlib
import hmac
import json
from typing import Any, Dict, Optional, Tuple

class TuyaApi:
    def __init__(
        self, endpoint: str, access_id: str, access_secret: str, lang: str = "en"
    ):
        self.client = httpx.AsyncClient(timeout=10.0)
        self.endpoint = endpoint
        self.access_id = access_id
        self.access_secret = access_secret
        self.lang = lang

    def _calculate_sign(
        self,
        access_token: str,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
    ) -> Tuple[str, int]:
        # HTTPMethod
        str_to_sign = method
        str_to_sign += "\n"

        # Content-SHA256
        content_to_sha256 = (
            "" if body is None or len(body.keys()) == 0 else json.dumps(body)
        )

        str_to_sign += (
            hashlib.sha256(content_to_sha256.encode("utf8")).hexdigest().lower()
        )
        str_to_sign += "\n"

        # Header
        str_to_sign += "\n"

        # URL
        str_to_sign += path

        if params is not None and len(params.keys()) > 0:
            str_to_sign += "?"

            query_builder = ""
            params_keys = sorted(params.keys())

            for key in params_keys:
                query_builder += f"{key}={params[key]}&"
            str_to_sign += query_builder[:-1]

        # Sign
        t = int(time.time() * 1000)

        message = self.access_id
        message += access_token
        message += str(t) + str_to_sign
        sign = (
            hmac.new(
                self.access_secret.encode("utf8"),
                msg=message.encode("utf8"),
                digestmod=hashlib.sha256,
            )
            .hexdigest()
            .upper()
        )
        return sign, t

    def __request(
        self,
        access_token: str,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        t = str(int(time.time() * 1000))

        sign, t = self._calculate_sign(access_token, method, path, params, body)
        headers = {
            "client_id": self.access_id,
            "sign": sign,
            "sign_method": "HMAC-SHA256",
            "access_token": access_token,
            "t": str(t),
            "lang": self.lang,
        }

        response = self.client.request(
            method=method,
            url=self.endpoint + path,
            params=params,
            headers=headers,
            content=body,
        )

        return response

    def get(
        self, access_token: str, path: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        return self.__request(access_token, "GET", path, params, None)


async def get_tuya_device(
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

    data = {"status": device_status.json(), "log": device_logs.json()}
    return data