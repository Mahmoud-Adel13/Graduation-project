
import sys
import socket
import selectors
import traceback
import time

import libclient


sel = selectors.DefaultSelector()

type_device = "traffic"


def create_request(type_mess, location, status, type_device):
    if type_mess == "warning" or type_mess == "update":
        return dict(
            type="text/json",
            encoding="utf-8",
            content=dict(type_mess=type_mess, location=location, status=status, type_device=type_device),
        )
    else: # type_mess == "devices_request" or type_mess == "status of traffic" or type_mess == "status of garage":
        return dict(
            type="text/json",
            encoding="utf-8",
            content=dict(type_mess=type_mess, type_device=type_device),
        )


def start_connection(host, port, request):
    addr = (host, port)
    print("starting connection to", addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = libclient.Message(sel, sock, addr, request)
    sel.register(sock, events, data=message)


host = "127.0.0.1"
port = 65432
type_mess = ("update", None, "update", None)
i = 0
location = 200
status = "ON"
request = create_request(type_mess, location, status, type_device)
start_connection(host, port, request)

try:
    while True:
        events = sel.select(timeout=1)
        for key, mask in events:
            message = key.data
            try:
                type_mess2 = type_mess[i]
                i = i+1
                location = 200
                status = "ON"
                request = create_request(type_mess2, location, status, type_device)
                message.process_events(mask, request)
                if i > 3:
                    i = 3

            except Exception:
                print(
                    "main: error: exception for",
                    f"{message.addr}:\n{traceback.format_exc()}",
                )
                message.close()
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()




