import sys
import socket
import selectors
import traceback
from time import *
import libserver

sel = selectors.DefaultSelector()


#########################################################################################
addr_Devices = {"addr_car1":"ip" , "addr_car2": "192.168.1.10", "addr_traffic": "192.168.1.8", "addr_garage": "ip"}
conn_Devices = {"sock_car1": None, "sock_car2": None, "sock_traffic": None, "sock_garage": None}
locations_dict = {"loc_car1": None, "loc_car2": None, "loc_traffic": None, "loc_garage": None}
speed_dict = {"speed_car1": None, "speed_car2": None}
status_dict = {"status_traffic": None, "status_garage": None, "status_car1": None, "status_car2": None}
Devices_info = {"conn_Devices": conn_Devices, "locations_dict": locations_dict, "speed_dict": speed_dict,
                "status_dict": status_dict}
message_obj = {"message_1": None, "message_2": None, "message_T": None, "message_g": None}
addr2 = None
timeouts = (None, 5)
i = 0
j = 0

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
    if addr[0] == addr_Devices["addr_car1"]:
        message_obj["message_1"] = libserver.Message(sel, conn, addr, **Devices_info)  ####################
        sel.register(conn, selectors.EVENT_READ, data=message_obj["message_1"])
        message = message_obj["message_1"]
    elif addr[0] == addr_Devices["addr_car2"]:
        message_obj["message_2"] = libserver.Message(sel, conn, addr, **Devices_info)  ####################
        sel.register(conn, selectors.EVENT_READ, data=message_obj["message_2"])
        message = message_obj["message_2"]
    elif addr[0] == addr_Devices["addr_traffic"]:
        message_obj["message_T"] = libserver.Message(sel, conn, addr, **Devices_info)  ####################
        sel.register(conn, selectors.EVENT_READ, data=message_obj["message_T"])
        message = message_obj["message_T"]
    elif addr[0] == addr_Devices["addr_garage"]:
        message_obj["message_g"] = libserver.Message(sel, conn, addr, **Devices_info)  ####################
        sel.register(conn, selectors.EVENT_READ, data=message_obj["message_g"])
        message = message_obj["message_g"]

    return message


host = "192.168.1.8"
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
        if events == [] :
            if message_obj["message_1"]:
                if message.addr == message_obj["message_1"].addr:
                    addr2 = message.addr
                    delete_device_info(addr2)
                    message_obj["message_1"].close()
                    message_obj["message_1"] = None
            if message_obj["message_2"]:
                if message.addr == message_obj["message_2"].addr:
                    addr2 = message.addr
                    delete_device_info(addr2)
                    message_obj["message_2"].close()
                    message_obj["message_2"] = None
            if message_obj["message_T"]:
                if message.addr == message_obj["message_T"].addr:
                    addr2 = message.addr
                    delete_device_info(addr2)
                    message_obj["message_T"].close()
                    message_obj["message_T"] = None
            if message_obj["message_g"]:
                if message.addr == message_obj["message_g"].addr:
                    addr2 = message.addr
                    delete_device_info(addr2)
                    message_obj["message_g"].close()
                    message_obj["message_g"] = None
            if j < 4:
                if list(message_obj.values())[j]:
                    message = message_obj[list(message_obj.items())[j][0]]
                else:
                    j = j + 1
            else:
                j = 0

        else:
            for key, mask in events:

                if key.data is None:
                    message = accept_wrapper(key.fileobj)
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
