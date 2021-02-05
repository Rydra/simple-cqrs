from simple_cqrs.domain_event import DomainEvent


class FruitCreated(DomainEvent):
    def __init__(self, id, name, occurred_on=None):
        super().__init__(occurred_on)
        self.id = id
        self.name = name
