from typing import Union,Callable
import json

class Receiver:
    _header_length = None
    _header = None

    def __init__(self, proto_header_len: int = 10):
        self._proto_header_length = proto_header_len
        self.buffer = ''

    def process(self, data) -> Union[None, str]:

        self.buffer += data.decode('utf-8')

        try:
            if not self._header_length and len(self.buffer) >= self._proto_header_length:
                self._process_decorator(self._process_proto_header, self._proto_header_length)

            if not self._header and len(self.buffer) >= self._header_length:
                self._process_decorator(self._process_header, self._header_length)

            if len(self.buffer) >= int(self._header['content-length']):
                msg = json.loads(self.buffer)
                self._clean()
                return msg
        except TypeError:
            pass
        return None

    def _process_decorator(self, process_f: Callable, start_index: int) -> None:
        process_f()
        self._truncate_buffer(start_index)

    def _process_proto_header(self) -> None:
        self._header_length = int(self.buffer[:self._proto_header_length].strip())

    def _process_header(self) -> None:
        self._header = json.loads(self.buffer[:self._header_length])

    def _truncate_buffer(self, start_index: int) -> None:
        self.buffer = self.buffer[start_index:]

    def _clean(self) -> None:
        self.buffer = ''
        self._header_length = None
        self._header = None

    def __repr__(self):
        return f'{self.__dict__}'