import json

class Sender:
    def __init__(self, content: str, proto_header_len: int = 10, **headers):
        self.content = {'data': content}

        self.headers = headers
        self.headers.update({'content-length': len(json.dumps(self.content))})

        self._proto_header_len = proto_header_len

    def get_message(self):
        header = self._prep_to_send(self.headers)
        message = self._prep_to_send(self.content)
        return f'{len(header):<{self._proto_header_len}}{header}{message}'.encode('utf-8')


    def _prep_to_send(self, header_or_content: dict):
        message = {key: value for key, value in header_or_content.items()}
        return json.dumps(message)

    def __repr__(self):
        return f'{self.__dict__}'