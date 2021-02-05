from hamcrest import *

from demo.commands import FruitCommandHandler, CreateFruit, CreateEventSourcedFruit
from demo.domain import Fruit, EventSourcedFruit
from demo.domain_listeners import FruitDomainEventHandler
from demo.repository import FruitRepository
from simple_cqrs.cqrs.command_bus import CommandBus
from simple_cqrs.domain_event_bus import DomainEventBus

repository = FruitRepository()
CommandBus().register_handler(FruitCommandHandler(repository))
DomainEventBus().reset()

# Each time a FruitCreated event is emitted, this handler will print
DomainEventBus().subscribe(FruitDomainEventHandler())

# Create a command and send to the CommandBus to dispatch it to the appropriate handler
# TODO: Here it would be a great place to introduce the correlation ID to identify and track the command
command = CreateFruit("banana")
id = CommandBus().send(command)

fruit = repository.get(id)

assert_that(fruit, is_(Fruit))
assert_that(fruit.name, is_("banana"))


# Now try with an eventsourced aggregate root
command = CreateEventSourcedFruit("banana")
id = CommandBus().send(command)

fruit = repository.get(id)

assert_that(fruit, is_(EventSourcedFruit))
assert_that(fruit.name, is_("banana"))
