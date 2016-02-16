
# Websockets with OtterSockets

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

2. Start the HTTP server (port 8000)

```sh
source ../pyenv/ui/bin/activate
python manage.py runserver
```

