import socket
import ssl


class URL:
    def __init__(self, url):
        # Split the url into two parts: the scheme and the hostname + path
        self.scheme, url = url.split("://", 1)
        assert self.scheme == "http" or self.scheme == "https"

        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443

        # Append a slash if only the hostname is provided
        if "/" not in url:
            url = url + "/"

        # Extract the hostname
        self.host, url = url.split("/", 1)

        # Check for custom port
        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

        # Extract the path
        self.path = "/" + url

    def make_request(self):
        new_socket = socket.socket(
            family=socket.AF_INET,  # IPv4
            type=socket.SOCK_STREAM,  # stream-oriented protocol
            proto=socket.IPPROTO_TCP,  # TCP
        )

        # Connect to the host
        new_socket.connect((self.host, self.port))

        if self.scheme == "https":
            ctx = ssl.create_default_context()
            new_socket = ctx.wrap_socket(new_socket, server_hostname=self.host)

        # Create and format request
        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "Connection: close\r\n"
        request += "User-Agent: Python Browser\r\n"
        request += "\r\n"

        # Convert to bytes and send the request
        new_socket.send(request.encode("utf8"))

        # Get the response
        response = new_socket.makefile("r", encoding="utf8", newline="\r\n")

        # Response status
        # Example: HTTP/1.1 200 OK
        status_line = response.readline()
        version, status_code, explanation = status_line.split(" ", 2)

        # Create a dictionary of header keys and values
        # Example: response_headers = {"content-type": "text/html", "content-length": "123"}
        response_headers = {}
        while True:
            new_line = response.readline()
            if new_line == "\r\n":
                break
            header, value = new_line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        content = response.read()
        new_socket.close()

        return content
