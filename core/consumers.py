# In consumers.py
from channels import Group
from channels.sessions import channel_session

# Connected to websocket.connect
@channel_session
def ws_connect(message):

    print ("--ws_connect")
    print (message)
    if "path" in message.content:
        listen_uuid = message.content["path"].split("/")[-1]

        print("Adding listener on [%s]" % (listen_uuid,))
        message.channel_session["uuid"] = listen_uuid
        Group("uuid-%s" % (listen_uuid,)).add(message.reply_channel)

@channel_session
def ws_add(message):
    print ("--ws_add")
    Group("uuid-%s" % (message.channel_session["uuid"],)).add(message.reply_channel)


def uuid_message(message):
    group_uuid = message.content["uuid"]
    print ("Processing update.uuid message to [%s]" % (group_uuid,))
    Group("uuid-%s" % (group_uuid,)).send(message.content)


# Connected to websocket.receive
@channel_session
def ws_message(message):
    print("--ws_message")
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    Group("chat").send(message.content)


# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    print("Received disconnect from %s" % (message.reply_channel,))
    Group("chat").discard(message.reply_channel)