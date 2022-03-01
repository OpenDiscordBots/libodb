from pydantic import BaseModel


class Guild(BaseModel):
    id: int
    banned: bool = False


class ServiceConfig(BaseModel):
    guild: Guild
    service: str
    data: dict


class JoinMessage(BaseModel):
    channel_id: int
    message_id: int


class Todo(BaseModel):
    id: int
    user_id: int
    task: str
    done: bool
    namespace: str
