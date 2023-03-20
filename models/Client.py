from pydantic import BaseModel


class IsStatusUpdate(BaseModel):
    name: str
    subscriber_id: str
    ip: str
    port_server: str
    user: str
    # passwd: str
    ip_server: str
    duration: str
    subscriber_number: str

    # updated_at: str
