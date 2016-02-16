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

##  Websockets with OtterSockets

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