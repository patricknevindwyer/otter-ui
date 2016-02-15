# Channels

- Channel per resolution (UUID for resolve)
- Channel per FQDN (recent updates/etc)
- Channel for service level heartbeats


# Running

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