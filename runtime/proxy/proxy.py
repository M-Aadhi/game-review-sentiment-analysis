"""Module providing proxy run function"""
import os

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json
import runtime.core as runtime
import sys
import site


def run(name: str, host: str = '', port: int = 3000, root=None, logFormat='normal'):
    """
        Run the application with the specified name on the specified host and port.

        Args:
            name (str): The name of the application to run.
            host (str, optional): The host IP address or hostname to bind the application to. Defaults to None.
            port (int, optional): The port number to bind the application to. Defaults to None.

        Returns:
            None

        """
    site_pkgs_path = site.getsitepackages()
    if site_pkgs_path in sys.path:
        sys.path.remove(site_pkgs_path)

    project_dir = os.getcwd()
    if root is not None and root.strip() != '':
        if os.path.isabs(root) is False:
            root = os.path.join(project_dir, root)
        project_dir = root

    site_pkgs_path = os.path.join(project_dir, '.venv', 'lib',
                                  f'python3.{sys.version_info.minor}', 'site-packages')
    sys.path.append(site_pkgs_path)

    runType = runtime.RunType.PROXY
    if logFormat == 'json':
        runType = runtime.RunType.AWS

    app = runtime.App(project_dir, runType)
    app.init_project()

    class ProxyRequestHandler(BaseHTTPRequestHandler):
        """
        A class representing a proxy request handler.

        This class inherits from BaseHTTPRequestHandler and overrides the do_POST and do_GET methods to handle HTTP POST and GET requests respectively.
        """

        def log_message(self, format, *args):
            pass

        def do_POST(self):
            """
            Handles HTTP POST requests.

            This method is called by the server when a client sends a POST request to the server.
            It sends a response with a 200 status code and the content of the file at the specified URI.
            """
            parsed_url = urllib.parse.urlparse(self.path)
            url = parsed_url.path
            if url == '/manifest.json':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(runtime.manifest().encode('utf-8'))
                return
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length).decode('utf-8')
            invoke_request = runtime.InvokeRequest(version=1,
                                                   protocol='HTTP',
                                                   method='POST',
                                                   url=url,
                                                   headers=dict(self.headers),
                                                   body=request_body,
                                                   is_base64_encoded=False)
            invoke_response = app.entry_handler(invoke_request)
            # Send response status code
            self.send_response(invoke_response.status_code)

            # Set response headers
            header = invoke_response.headers
            if header is not None:
                for header, value in header.items():
                    self.send_header(header, value)
                self.end_headers()
            self.wfile.write(invoke_response.body.encode('utf-8'))

        def do_GET(self):
            """
            Handles HTTP GET requests.

            This method is called by the server when a client sends a GET request to the server.
            It sends a response with a 200 status code and the content of the file at the specified URI.
            """
            parsed_url = urllib.parse.urlparse(self.path)
            uri = parsed_url.path
            if uri == '/manifest.json':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(app.manifest_content.encode('utf-8'))
                return
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Not found')
                return

    httpd = HTTPServer((host, port), ProxyRequestHandler)
    try:
        # 启动HTTP服务器
        with httpd:
            print(f'Server started on {host}:{port}')
            # 进入服务器的主循环
            httpd.serve_forever()
    except KeyboardInterrupt:
        # 捕获Ctrl+C事件
        print("Server stopped")
        httpd.server_close()
