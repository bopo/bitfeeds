from websocket_server import WebsocketServer
import json

# Called for every storage connecting (after handshake)
def new_storage(storage, server):
	print("New storage connected and was given id %d" % storage['id'])
	server.send_message_to_all(json.dumps({"new_storage": storage['id']}))


# Called for every storage disconnecting
def storage_left(storage, server):
	print("Client(%d) disconnected" % storage['id'])


# Called when a storage sends a message
def message_received(storage, server, message):
	if len(message) > 200:
		message = message[:200]+'..'
	
	print("Client(%d) said: %s" % (storage['id'], message))


PORT=1440
server = WebsocketServer(PORT)
server.set_fn_new_storage(new_storage)
server.set_fn_storage_left(storage_left)
server.set_fn_message_received(message_received)
server.run_forever()
