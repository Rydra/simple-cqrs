from demo.events import FruitCreated
from simple_cqrs.cqrs.domain import EventSourcedAggregateRoot, mutator


class Fruit:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class EventSourcedFruit(EventSourcedAggregateRoot):
    @mutator
    def on_created(self, event: FruitCreated):
        self.name = event.name
        self.id = event.id

    @classmethod
    def create(cls, id, name):
        return EventSourcedAggregateRoot._create(
            cls,
            FruitCreated(id, name)
        )
