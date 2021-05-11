import sys
import socket
import selectors
import traceback

import libserver

sel = selectors.DefaultSelector()


#########################################################################################
addr_Devices = {"addr_car1": "127.0.0.1", "addr_car2": "127.0.0.1", "addr_traffic": "ip", "addr_garage": "ip"}
conn_Devices = {"sock_car1": None, "sock_car2": None, "sock_traffic": None, "sock_garage": None}
locations_dict = {"loc_car1": None, "loc_car2": None, "loc_traffic": None, "loc_garage": None}
speed_dict = {"speed_car1": None, "speed_car2": None}
status_dict = {"status_traffic": None, "status_garage": None, "status_car1": None, "status_car2": None}
Devices_info = {"conn_Devices": conn_Devices, "locations_dict": locations_dict, "speed_dict": speed_dict,
                "status_dict": status_dict}
message_obj = {"message_1": None, "message_2": None, "message_T": None, "message_g": None}
type_device={}
addr2 = None
timeouts = (None, 5)
i = 0


def connection_devices(conn, addr):
    if addr[0] == addr_Devices["addr_car1"]:
        conn_Devices["sock_car1"] = conn
    elif addr[0] == addr_Devices["addr_car2"]:
        conn_Devices["sock_car2"] = conn
    elif addr[0] == addr_Devices["addr_traffic"]:
        conn_Devices["sock_traffic"] = conn
    elif addr[0] == addr_Devices["addr_garage"]:
        conn_Devices["sock_garage"] = conn


def delete_device_info(addr2):
    if addr2[0] == addr_Devices["addr_car1"]:
        conn_Devices["sock_car1"] = None
        locations_dict["loc_car1"] = None
        speed_dict["speed_car1"] = None
        status_dict["status_car1"] = None
    elif addr2[0] == addr_Devices["addr_car2"]:
        conn_Devices["sock_car2"] = None
        locations_dict["loc_car2"] = None
        speed_dict["speed_car2"] = None
        status_dict["status_car2"] = None
    elif addr2[0] == addr_Devices["addr_traffic"]:
        conn_Devices["sock_traffic"] = None
        locations_dict["loc_traffic"] = None
        status_dict["status_traffic"] = None
    elif addr2[0] == addr_Devices["addr_garage"]:
        conn_Devices["sock_garage"] = None
        locations_dict["loc_garage"] = None
        status_dict["status_garage"] = None

#################################################################################################


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    connection_devices(conn, addr)                                #######################
    message = libserver.Message(sel, conn, addr, **Devices_info)  ####################
    sel.register(conn, selectors.EVENT_READ, data=message)


host = "127.0.0.1"
port = 65432

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:

    while True:

        events = sel.select(timeout=timeouts[i])
        i = 1
        if events == []:
            if message.sock:
                addr2 = message.addr
                delete_device_info(addr2)
                message.close()
        else:
            for key, mask in events:

                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    message = key.data
                    try:
                        message.process_events(mask)

                    except Exception:
                        print(
                            "main: error: exception for",
                            f"{message.addr}:\n{traceback.format_exc()}",
                        )
                        message.close()


except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
