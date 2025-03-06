from bson import ObjectId
from pydantic import BaseModel, Field

from core.domain.events import DomainEvent
from core.domain.value_objects import PydanticObjectId


class Entity(BaseModel):
    id: PydanticObjectId = Field(default_factory=ObjectId, alias="_id")


class Aggregate(Entity):
    events: list = Field(default_factory=list)

    def register_event(self, event: DomainEvent):
        self.events.append(event)

    def collect_events(self):
        events = self.events
        self.events = []
        return events
