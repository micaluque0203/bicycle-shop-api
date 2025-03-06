from pydantic import BaseModel


class DomainEvent(BaseModel):
    def __next__(self):
        yield self
