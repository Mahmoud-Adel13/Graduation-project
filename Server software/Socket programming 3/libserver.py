import sys
import selectors
import json
import io
import struct
import time

### Global dectionaries:
Devices_number = {"cars": 0, "traffic": 0, "garage": 0}                                                     # number of connected sevices to server
conn_Devices = {"sock_car1": None, "sock_car2": None, "sock_traffic": None, "sock_garage": None}            # connected-devices sockets' ip
locations_dict = {"loc_car1": None, "loc_car2": None, "loc_traffic": None, "loc_garage": None}
speed_dict = {"speed_car1": None, "speed_car2": None}                                                       # connected cars speed dict
status_dict = {"status_traffic": None, "status_garage": None, "status_car1": None, "status_car2": None}     # Connected device status dict
Devices_info = {"conn_Devices": conn_Devices, "locations_dict": locations_dict, "speed_dict": speed_dict,
                "status_dict": status_dict}                                                                 # All device info for each connected device dict

class Message:

    def __init__(self, selector, sock, addr, **Devices_info):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_buffer = b""
        self._send_buffer = b""
        self._jsonheader_len = None
        self.jsonheader = None
        self.request = None
        self.response_created = False
        ############################################################
        self.conn_Devices = Devices_info["conn_Devices"]
        self.locations_dict = Devices_info["locations_dict"]
        self.speed_dict = Devices_info["speed_dict"]
        self.status_dict = Devices_info["status_dict"]
        ###########################################################



    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""

        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {repr(mode)}.")
        self.selector.modify(self.sock, events, data=self)

    def _read(self):
        try:
            # Should be ready to read
            data = self.sock.recv(4096)

        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            if data:
                self._recv_buffer += data

            else:
                raise RuntimeError("Peer closed.")

    def _write(self, sock):
        if self._send_buffer:

            print("sending", repr(self._send_buffer), "to", sock.getpeername())
            #sock.getpeername() instead of (self.addr)
            try:
                # Should be ready to write

                sent = sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]
                # Close when the buffer is drained. The response has been sent.

                if sent and not self._send_buffer:
                    Devices_info = {"conn_Devices": self.conn_Devices, "locations_dict": self.locations_dict,
                                    "speed_dict": self.speed_dict,
                                    "status_dict": self.status_dict}
                    self.__init__(self.selector, self.sock, self.addr, **Devices_info)
                    self._set_selector_events_mask("r")

    def _json_encode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

    def _json_decode(self, json_bytes, encoding):
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        obj = json.load(tiow)
        tiow.close()
        return obj

    def _create_message(
        self, *, content_bytes, content_type, content_encoding
    ):
        jsonheader = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
        }
        jsonheader_bytes = self._json_encode(jsonheader, "utf-8")
        message_hdr = struct.pack(">H", len(jsonheader_bytes))
        message = message_hdr + jsonheader_bytes + content_bytes
        return message
########################################################################################

    def create_data_object(self, type_device, location, speed, status):
        if type_device == "car_1":
            self.locations_dict["loc_car1"] = location
            self.speed_dict["speed_car1"] = speed
            self.status_dict["status_car1"] = status

        elif type_device == "car_2":
            self.locations_dict["loc_car2"] = location
            self.speed_dict["speed_car2"] = speed
            self.status_dict["status_car2"] = status

        elif type_device == "traffic":
            self.locations_dict["loc_traffic"] = location
            self.status_dict["status_traffic"] = status

        elif type_device == "garage":
            self.locations_dict["loc_garage"] = location
            self.status_dict["status_garage"] = status

        answer = f' Successfully updated.'

        return answer

    def create_warning(self, type_device, location):
        range = 300
        if type_device == "car_1":
            self.locations_dict["loc_car1"] = location
            if self.locations_dict["loc_car2"] != None:
                if (self.locations_dict["loc_car2"] <= (self.locations_dict["loc_car1"] + range)) & (self.locations_dict["loc_car2"] > (self.locations_dict["loc_car1"] - range)):
                    answer = f' there is warning from car1   "status: {self.status_dict["status_car1"]}".'
                    sock = self.conn_Devices["sock_car2"]
                else:
                    answer = f' not car in range.'
                    sock = self.conn_Devices["sock_car1"]
            else:
                answer = f' not car in range.'
                sock = self.conn_Devices["sock_car1"]

        elif type_device == "car_2":
            self.locations_dict["loc_car2"] = location
            if self.locations_dict["loc_car1"] != None:
                if (self.locations_dict["loc_car1"] <= (self.locations_dict["loc_car2"] + range)) & (self.locations_dict["loc_car1"] > (self.locations_dict["loc_car2"] - range)):
                    answer = f' there is warning from car2  "status: {self.status_dict["status_car2"]}".'
                    sock = self.conn_Devices["sock_car1"]
                else:
                    answer = f' not car in range.'
                    sock = self.conn_Devices["sock_car2"]
            else:
                answer = f' not car in range.'
                sock = self.conn_Devices["sock_car2"]

        return answer, sock

    def create_devices_request(self, type_device):
        if type_device == "car_1":
            location = self.locations_dict["loc_car1"]
            del self.locations_dict["loc_car1"]
            answer = f'locations of Devices "{self.locations_dict}".'
            self.locations_dict["loc_car1"] = location

        elif type_device == "car_2":
            location = self.locations_dict["loc_car2"]
            del self.locations_dict["loc_car2"]
            answer = f'locations of Devices "{self.locations_dict}".'
            self.locations_dict["loc_car2"] = location

        return answer

    def status_of_traffic(self, sstatus, location_T):
        answer = f' status of traffic "{sstatus}" location "{location_T}".'
        return answer

    def status_of_garage(self, sstatus, location_g):
        answer = f' status of garage "{sstatus}"  location "{location_g}".'
        return answer

    def _create_response_json_content(self):
        type_device = self.request.get("type_device")
        location = self.request.get("location")
        speed = self.request.get("speed")
        status = self.request.get("status")
        type_mess = self.request.get("type_mess")

        if type_mess == "warning":
            answer = self.create_warning(type_device, location)[0]
            sock = self.create_warning(type_device, location)[1]

        elif type_mess == "devices_request":
            answer = self.create_devices_request(type_device)
            sock = self.sock

        elif type_mess == "status of traffic":
            location_T = self.locations_dict["loc_traffic"]
            sstatus = self.status_dict["status_traffic"]
            answer = self.status_of_traffic(sstatus, location_T)
            sock = self.sock

        elif type_mess == "status of garage":
            location_g = self.locations_dict["loc_garage"]
            sstatus = self.status_dict["status_garage"]
            answer = self.status_of_garage(sstatus, location_g)
            sock = self.sock

        elif type_mess == "update":
            answer = self.create_data_object(type_device, location, speed, status)
            sock = self.sock

        content = {"result": answer}
        content_encoding = "utf-8"
        response = {
            "content_bytes": self._json_encode(content, content_encoding),
            "content_type": "text/json",
            "content_encoding": content_encoding,
        }
        return response, sock
#########################################################################################

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        self._read()
        if self._jsonheader_len is None:
            self.process_protoheader()

        if self._jsonheader_len is not None:
            if self.jsonheader is None:
                self.process_jsonheader()

        if self.jsonheader:
            if self.request is None:
                self.process_request()

    def write(self):
        if self.request:
            if not self.response_created:
                sock = self.create_response()

        self._write(sock)  ##################################

    def close(self):
        try:

            self.selector.unregister(self.sock)
            print("closing connection to", self.addr)
        except Exception as \
                e:
            print(
                "error: selector.unregister() exception for",
                f"{self.addr}: {repr(e)}",
            )

        try:
            self.sock.close()
        except OSError as e:
            print(
                "error: socket.close() exception for",
                f"{self.addr}: {repr(e)}",
            )
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None

    def process_protoheader(self):
        hdrlen = 2
        if len(self._recv_buffer) >= hdrlen:
            self._jsonheader_len = struct.unpack(">H", self._recv_buffer[:hdrlen])[0]
            self._recv_buffer = self._recv_buffer[hdrlen:]

    def process_jsonheader(self):
        hdrlen = self._jsonheader_len
        if len(self._recv_buffer) >= hdrlen:
            self.jsonheader = self._json_decode(
                self._recv_buffer[:hdrlen], "utf-8"
            )
            self._recv_buffer = self._recv_buffer[hdrlen:]
            for reqhdr in (
                    "byteorder",
                    "content-length",
                    "content-type",
                    "content-encoding",
            ):
                if reqhdr not in self.jsonheader:
                    raise ValueError(f'Missing required header "{reqhdr}".')

    def process_request(self):
        content_len = self.jsonheader["content-length"]
        if not len(self._recv_buffer) >= content_len:
            return
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]

        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            self.request = self._json_decode(data, encoding)

            print("received request", repr(self.request), "from", self.addr)
        else:
            # Binary or unknown content-type
            self.request = data
            print(
                f'received {self.jsonheader["content-type"]} request from',
                self.addr,
            )
        # Set selector to listen for write events, we're done reading.
        self._set_selector_events_mask("w")

    def create_response(self):
        if self.jsonheader["content-type"] == "text/json":
            response = self._create_response_json_content()[0]
            sock = self._create_response_json_content()[1]

        message = self._create_message(**response)
        self.response_created = True
        self._send_buffer += message
        return sock
