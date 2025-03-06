from core.domain.events import DomainEvent
from core.domain.value_objects import PydanticObjectId


class OrderCreatedEvent(DomainEvent):
    order_id: PydanticObjectId
