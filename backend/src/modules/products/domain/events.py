from core.domain.events import DomainEvent
from core.domain.value_objects import PydanticObjectId


class ProductCreatedEvent(DomainEvent):
    product_id: PydanticObjectId


class ProductUpdatedEvent(DomainEvent):
    product_id: PydanticObjectId


class ProductDeletedEvent(DomainEvent):
    product_id: PydanticObjectId


class PartCreatedEvent(DomainEvent):
    part_id: PydanticObjectId


class PartUpdatedEvent(DomainEvent):
    part_id: PydanticObjectId


class PartDeletedEvent(DomainEvent):
    part_id: PydanticObjectId


class ConfigurationRuleCreatedEvent(DomainEvent):
    rule_id: PydanticObjectId


class ConfigurationRuleUpdatedEvent(DomainEvent):
    rule_id: PydanticObjectId


class ConfigurationRuleDeletedEvent(DomainEvent):
    rule_id: PydanticObjectId
