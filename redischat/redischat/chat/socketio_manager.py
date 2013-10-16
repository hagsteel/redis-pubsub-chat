from django.http import HttpResponse
from socketio import socketio_manage
from .chat_socketio import ChatNamespace


def socketio(request):
    socketio_manage(request.environ,
        {
            '/chat': ChatNamespace,
        }, request=request
    )

    return HttpResponse()
