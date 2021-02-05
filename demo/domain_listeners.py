from demo.events import FruitCreated
from simple_cqrs.domain_subscriber import DomainEventHandler, event_handler


class FruitDomainEventHandler(DomainEventHandler):
    @event_handler
    def on_fruit_created(self, event: FruitCreated):
        print(f"Hey! I created the fruit {event.name}!")
