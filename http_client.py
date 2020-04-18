import re
import socket


class Response:
    body: str = None
    response_code: int = None
    headers: dict = {}
    raw: bytes = None

    def __init__(self, response_content: bytes):
        self.raw = response_content

        str_response = response_content.decode('utf-8', errors='ignore')
        response_info, self.body = str_response.split('\r\n\r\n', 1)
        response_status, response_headers = response_info.split('\r\n', 1)

        self.response_code = int(re.search(r' (\d{3}) ', response_status).group(1))

        response_headers = response_headers.split('\r\n')
        for header in response_headers:
            key, value = header.split(': ')
            self.headers[key] = value


class HttpClient:
    user_agent = 'pyhttpclient/0.0.1'

    def request(
        self,
        method: str,
        host: str,
        port: int = 80,
        path: str = None,
        headers: dict = None,
        body: str = None,
    ) -> Response:
        method = method.upper()

        if not path:
            path = '/'
        elif not path.startswith('/'):
            path = f'/{path}'

        request_data = [
            f'{method} {path} HTTP/1.1',
            f'Host: {host}',
            f'User-Agent: {self.user_agent}',
            'Accept: */*',
            'Connection: close',
        ]

        if headers:
            for key, value in headers.items():
                request_data.append(f'{key}: {value}')

        request = '\r\n'.join(request_data)
        request += '\r\n\r\n'

        if body:
            request += body

        request = request.encode('utf-8')

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.send(request)

        response = b''
        while True:
            chunk = sock.recv(1024)
            if not chunk:
                break
            response += chunk

        sock.close()
        return Response(response)
