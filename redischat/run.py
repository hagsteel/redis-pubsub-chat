#!/usr/bin/env python
from gevent import monkey
from socketio.server import SocketIOServer
import django.core.handlers.wsgi
import os
import sys

monkey.patch_all()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "redischat.settings")
if not os.environ.get('DJANGO_CONFIGURATION'):
    os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

PORT = 9000

if __name__ == '__main__':
    print 'Listening on http://0.0.0.0:%s and on port 843 (flash policy server)' % PORT
    SocketIOServer(('0.0.0.0', PORT), application, resource="socket.io").serve_forever()
