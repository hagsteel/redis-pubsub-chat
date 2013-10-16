from django.conf.urls import patterns, include, url
from .chat.socketio_manager import socketio
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='chat.html'), name='chat'),
    url("^socket\.io", socketio, name='socketio'),
)

urlpatterns += staticfiles_urlpatterns()
