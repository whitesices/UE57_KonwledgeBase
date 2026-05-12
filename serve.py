"""UE57 Knowledge Base Browser Server
Usage:   python serve.py
Open:    http://localhost:8765/knowledge-browser.html
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket, os

PORT = 8765

class UTF8Handler(SimpleHTTPRequestHandler):
    def send_header(self, key, value):
        if key.lower() == 'content-type' and 'text' in value and 'charset' not in value:
            value += '; charset=utf-8'
        super().send_header(key, value)

os.chdir(r'C:\UEWork\UnrealEngine-5.7.4-release\UE57_KnowledgeBase')

class Server(HTTPServer):
    allow_reuse_address = True
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        super().server_bind()

print(f'\n  UE57 Knowledge Base Browser')
print(f'  http://localhost:{PORT}/knowledge-browser.html')
print(f'  Press Ctrl+C to stop\n')

try:
    Server(('', PORT), UTF8Handler).serve_forever()
except KeyboardInterrupt:
    print('\nServer stopped.')
