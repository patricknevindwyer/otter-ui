# Running Otter

The Otter application is comprised of a Django based front end, and a bevy of NodeJS
based microservices for content resolution, analysis, and interaction.

The Django front end provides basic UI and layout, as well as a kick start for service
resolution, historics, and search.

Each of the micro services provides a data source that informs one or more of the pipeline
components viewable in Otter.

## UI

1. Start the HTTP server (port 8000)

```sh
source ../pyenv/ui/bin/activate
python manage.py runserver
```

## Dispatch

The Dispatch service provides distributed and asynchronous service discovery for Otter,
using either service name (service-whois) or service group (dns, ip, headers, etc) 
listeners that notifiy registered listeners via async webhooks.

NodeJS components can interface with Dispatch using the __TODO: package name here__ Node
package, while Python components can use the __TODO: package name here__ Python package.

TODO: Name will be OtterBall

## Services

DNS

Cached DNS
Google DNS
OpenNIC DNS
Local ASN
WHOIS

##  Websockets with OtterSockets and Catflap

Integrating a websockets layer with the Django front end is a non trivial task, especially
with asynchronous service resolution. To address this, Otter breaks things down into a
handful of layers, each responsible for a different portion of the Websockets lifecycle.

First is the client side Socket layer, which is served up via the Django front end as
part of the normal request cycle. The client layer will attempt to create a websockets
connection to the OtterSockets API. 

OtterSockets handles the coordination of socket layers and sending and receiving messages
from the client layer. OtterSockets multiplexes and balances socket handling across multiple
services and instances using the Socket.io-Emitter, which is a Redis backed pooling
library.

Sending messages from the server to the client is handled by the CatFlap API. CatFlap is
a combination of a standard RESTful service and a WebSockets layer service. Wearing these
two hats, CatFlap serves as the translation layer between the Restful and WebSockets worlds.

Messages bound for websockets on the backend are routed via UUID and FQDN. None, one, or many
users may be subscribed to a FQDN or UUID channel, and any subscribers will get notified
when there is a status update for the associated UUID or FQDN. 

Any service on the backend can send a well formed RESTful message to CatFlap, which will
publish the message across the translation layer. OtterSockets will then distributed the
published message to any listeners for that UUID or FQDN.

0. Check that Redis is running

```sh
./redis-server
```


1. Make sure OtterSockets is running

```sh
export PORT=2222 && node otterSockets.js
```


2. Make sure the Catflap transition layer is running

```sh
export PORT=3333 && npm start
```


# Writing Services

* Service Groups (DNS, IP, etc)
* Webhooks to UI
* Config webhooks
* find an open port/lookup