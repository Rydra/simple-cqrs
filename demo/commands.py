import uuid

from demo.domain import Fruit, EventSourcedFruit
from demo.repository import FruitRepository
from simple_cqrs.cqrs.domain import AggregateId
from simple_cqrs.cqrs.handlers import Command, CommandHandler, command_handler


class CreateFruit(Command):
    def __init__(self, name):
        self.name = name


class CreateEventSourcedFruit(Command):
    def __init__(self, name):
        self.name = name


class FruitCommandHandler(CommandHandler):
    def __init__(self, repository: FruitRepository):
        self.fruit_repository = repository

    @command_handler
    def create_fruit(self, command: CreateFruit):
        fruit = Fruit(AggregateId.generate(), command.name)
        self.fruit_repository.save(fruit)
        return fruit.id

    @command_handler
    def create_eventsourced_fruit(self, command: CreateEventSourcedFruit):
        fruit = EventSourcedFruit.create(AggregateId.generate(), command.name)

        # You usually emit all the events inside a fruit when the events have been saved successfully
        self.fruit_repository.save(fruit)
        return fruit.id
