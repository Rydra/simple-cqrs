from simple_cqrs.cqrs.domain import EventSourcedAggregateRoot


class FruitRepository:
    """
    An in-memory repository. Here you can use whatever repository you want
    """
    def __init__(self):
        self.items = {}

    def save(self, agg):
        self.items[agg.id] = agg
        if isinstance(agg, EventSourcedAggregateRoot):
            for event in agg._changes:
                # Emitting the events so that the changes are propagated to the domain event handlers
                event.emit()
            agg._changes.clear()

    def get(self, id):
        return self.items.get(id)
