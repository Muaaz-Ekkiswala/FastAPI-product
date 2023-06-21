from pydantic import BaseModel as PydenticBaseModel


class BaseModel(PydenticBaseModel):
    class Config:
        orm_mode = True