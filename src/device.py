from pydantic import BaseModel
from typing import List, Optional


class StatusItem(BaseModel):
    code: str
    value: str | int | float | bool

    model_config = {"extra": "forbid"}


class StatusResult(BaseModel):
    active_time: int
    biz_type: int
    category: str
    create_time: int
    icon: str
    id: str
    ip: str
    lat: str
    local_key: str
    lon: str
    model: str
    name: str
    online: bool
    owner_id: str
    product_id: str
    product_name: str
    status: List[StatusItem]
    sub: bool
    time_zone: str
    uid: str
    update_time: int
    uuid: str

    model_config = {"extra": "forbid"}


class StatusWrapper(BaseModel):
    result: StatusResult
    success: bool
    t: int
    tid: str

    model_config = {"extra": "forbid"}


class LogItem(BaseModel):
    code: str
    event_time: int
    value: str | int | float | bool

    model_config = {"extra": "forbid"}


class LogResult(BaseModel):
    device_id: str
    has_more: bool
    logs: List[LogItem]
    total: int

    model_config = {"extra": "forbid"}


class LogWrapper(BaseModel):
    result: LogResult
    success: bool
    t: int
    tid: str

    model_config = {"extra": "forbid"}


class Root(BaseModel):
    status: StatusWrapper
    log: LogWrapper

    model_config = {"extra": "forbid"}


import json

your_json_string = """
{
  "status": {
    "result": {
      "active_time": 1761834594,
      "biz_type": 18,
      "category": "sj",
      "create_time": 1761834594,
      "icon": "smart/icon/ay1559113396016bSygG/f3cb8a2c7d7f737f6667ba8f2bc3bef2.jpg",
      "id": "bf633bc8f6e7aab5f3sjip",
      "ip": "217.131.154.221",
      "lat": "40.98",
      "local_key": "fH!!{B0|9p&8;v[1",
      "lon": "28.79",
      "model": "WG-092",
      "name": "water leak sensor ",
      "online": true,
      "owner_id": "259230565",
      "product_id": "bw94azhcnjeu1i0v",
      "product_name": "water leak sensor ",
      "status": [
        {
          "code": "watersensor_state",
          "value": "normal"
        },
        {
          "code": "battery_percentage",
          "value": ["5"]
        }
      ],
      "sub": false,
      "time_zone": "+03:00",
      "uid": "eu1761833692098J4s7T",
      "update_time": 1763107974,
      "uuid": "6f73ab54f4fd934d"
    },
    "success": true,
    "t": 1763129772647,
    "tid": "7964cbf5c16411f08e5dda57e8f5d0ed"
  },
  "log": {
    "result": {
      "device_id": "bf633bc8f6e7aab5f3sjip",
      "has_more": false,
      "logs": [
        {
          "code": "battery_percentage",
          "event_time": 1763107974230,
          "value": "96"
        },
        {
          "code": "battery_percentage",
          "event_time": 1763079160887,
          "value": "100"
        },
        {
          "code": "battery_percentage",
          "event_time": 1763050345452,
          "value": "100"
        },
        {
          "code": "battery_percentage",
          "event_time": 1763021525700,
          "value": "100"
        },
        {
          "code": "battery_percentage",
          "event_time": 1762992720622,
          "value": "99"
        },
        {
          "code": "battery_percentage",
          "event_time": 1762963928363,
          "value": "100"
        },
        {
          "code": "battery_percentage",
          "event_time": 1762935112947,
          "value": "97"
        },
        {
          "code": "battery_percentage",
          "event_time": 1762906312755,
          "value": "100"
        },
        {
          "code": "battery_percentage",
          "event_time": 1762877520240,
          "value": "97"
        },
        {
          "code": "battery_percentage",
          "event_time": 1762848707552,
          "value": "97"
        },
        {
          "code": "battery_percentage",
          "event_time": 1762819891724,
          "value": "100"
        },
        {
          "code": "battery_percentage",
          "event_time": 1762791076295,
          "value": "97"
        },
        {
          "code": "battery_percentage",
          "event_time": 1762762260725,
          "value": "98"
        },
        {
          "code": "battery_percentage",
          "event_time": 1762733445093,
          "value": "100"
        },
        {
          "code": "battery_percentage",
          "event_time": 1762704629906,
          "value": "100"
        }
      ],
      "total": 1000
    },
    "success": true,
    "t": 1763129772902,
    "tid": "7975b426c16411f0a25e9ed280a40f39"
  }
}
"""

data = json.loads(your_json_string)

obj = Root(**data)

print(obj.status.result.name)
print(obj.log.result.logs[0].event_time)