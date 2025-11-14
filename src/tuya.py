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
