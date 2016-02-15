
# Websockets with Django Channels

## Channels

- Channel per resolution (UUID for resolve)
- Channel per FQDN (recent updates/etc)
- Channel for service level heartbeats


## Running

1. Start the websockets server (port 9000)

```sh
source ../pyenv/ui/bin/activate
python manage.py runwsserver
```

2. Start the HTTP server (port 8000)

```sh
source ../pyenv/ui/bin/activate
python manage.py runserver
```

3. Start worker(s)

```sh
source ../pyenv/ui/bin/activate
python manage.py runworker
```

## Resources

http://channels.readthedocs.org/en/stable/getting-started.html

https://github.com/andrewgodwin/channels/tree/0.8/channels

http://www.slideshare.net/daikeren/django-channels

https://github.com/daikeren/channel-example/blob/master/chat/chat/settings.py

http://autobahn.ws/python/reference/autobahn.websocket.html