# Simple CQRS

## A small library to create CQRS and event-driven architectures in python

## Basic usage


In addition, Melange supports event driven architectures in single-process, non-distributed, memory-based applications (Console applications, background workers)
with the aid of the `DomainEventBus` (see `Domain-Driven Design` section). The `DomainEventBus` is great if you really 
want to have a clean event-driven architecture with Domain Events, and its idea has been grabbed from Vaughn Vernon and his must-read book 
Implementing Domain-Driven Design (look at [part 3 of these series](http://dddcommunity.org/library/vernon_2011/) if you want a quick look,
 or read this excellent article from [Udi Dahan, founder of NServiceBus](http://udidahan.com/2009/06/14/domain-events-salvation/)).

## Installing ##

Execute the following two commands to install melange in your system (working in packaging this to combine both
commands into a single one):

```
pip install git+https://github.com/Rydra/redis-simple-cache.git/@master
pip install melange
```

## How to get started ##

Event-driven architectures work with the Publish/Subscribe pattern to achieve decoupling.
With this pattern, publishers and subscribers do not know about each other while they can exchange
information among them. In order to achieve this and communicate effectively a 
mediator, or better said, a **Message Broker** is required to transfer messages from
publishers to subscribers. Clients can subscribe this broker, waiting for events they are interested in,
or publish messages so that the broker can distribute these messages appropriately.

So, you will need two things to make this entire scene work: an **Exchange Message Publisher** and
an **Exchange Message Consumer** to send and receive messages respectively.

But before getting your feet wet into this realm, first things first. You need to tell Melange which driver backend
you want to use. Place this line in the initialization code of your application:


So, what's going on here? We've created a **Listener** that is interested in events of type
`ProductAdded` and will react to those events when received from the Message Broker. Override
`process` to provide behavior, and override `listens_to` to provide an array of event names you are
interested in.

We will attach this listener to a **queue**. A queue is a place where the messages received from
SNS will be stored and available for the consumer application at his own time. To do so, we first create
an `ExchangeMessageConsumer` with a queue name and a topic. If the queue does not exist, it will create
an **SQS queue** and subscribe it to the topic. 

Afterwards, you can subscribe an instance of your listener to the message consumer. Finally, you
create a loop that will poll for new events and invoke the `process` method of your ExchangeListener
for each event of the expected type it receives.

### Domain-Driven Design

In his book "Implementing Domain-Driven Design", in Chapter 8 when talking about Domain Events describes
an implementation of a `Domain Event Publisher`. Domain Events are part of the ubiquitous language and
part of your Domain, and your domain should be abstracted from implementation details like your messaging
framework. This is why I decided to integrate here a `DomainEventBus`.

The `DomainEventBus` is intended to be used inside your Domain Model as the mecanism to publish
Domain Events and forward them to interested parties. DO NOT confuse this concept of Bus with 
Publish/Subscribe to a Message Broker like RabbitMQ or Amazon SNS+SQS. This bus lives in the same
thread as the entity or domain service that implements your Domain Model.

An example of use:

```python
class MySubscriber(DomainSubscriber):
	def process(self, event):
		print (f"{event.product_id}{event.name}")
		
	def listens_to(self):
		return [ ProductAddedDomainEvent ]
		

DomainEventBus.instance().reset() # Remember to always reset the bus prior to usage in the current thread

DomainEventBus.instance().subscribe(MySubscriber())

# ... inside your business logic at some point ...

product_repository.add(my_product)
DomainEventBus.instance().publish(ProductAddedDomainEvent(my_product.id, my_product.name))
```

If you wanna learn more about how to do clean architectures and domain well isolated from
your technology stack I advise, again, to read *Implementing Domain-Driven Design* from Vaughn Vernon
and *Clean Architecture* from Uncle Bob
