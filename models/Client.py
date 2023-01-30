from pydantic import BaseModel


class IsStatusUpdate(BaseModel):
    status: int
    # updated_at: str
