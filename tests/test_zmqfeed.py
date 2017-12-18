import zmq

context = zmq.Context()
sock = context.socket(zmq.SUB)

# sock.connect("ipc://marketfeed")
sock.connect("tcp://127.0.0.1:6001")
sock.setsockopt_string(zmq.SUBSCRIBE, '')

print("Started...")

while True:
    ret = sock.recv_pyobj()
    print(ret)
