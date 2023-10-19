from pydantic import BaseModel


class IsScheduler(BaseModel):
    sites_id: str
    tipe: str
    timee: str
    duration: str
