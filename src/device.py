from pydantic import BaseModel
from typing import List, Union

class StatusItem(BaseModel):
    code: str
    value: Union[str, int, float, bool]

    class Config:
        extra = "forbid"


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

    class Config:
        extra = "forbid"


class StatusWrapper(BaseModel):
    result: StatusResult
    success: bool
    t: int
    tid: str

    class Config:
        extra = "forbid"


class LogItem(BaseModel):
    code: str
    event_time: int
    value: Union[str, int, float, bool]

    class Config:
        extra = "forbid"


class LogResult(BaseModel):
    device_id: str
    has_more: bool
    logs: List[LogItem]
    total: int

    class Config:
        extra = "forbid"


class LogWrapper(BaseModel):
    result: LogResult
    success: bool
    t: int
    tid: str

    class Config:
        extra = "forbid"


class Device(BaseModel):
    status: StatusWrapper
    log: LogWrapper

    class Config:
        extra = "forbid"