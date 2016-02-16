from core.consumers import ws_add, ws_message, ws_disconnect, uuid_message, ws_connect

# Routing is in SETTINGS.PY
channel_routing = {
    "websocket.connect": ws_connect,
    "websocket.receive": ws_message,
    "websocket.disconnect": ws_disconnect,
    "websocket.keepalive": ws_add,
    "update-uuid": uuid_message
}