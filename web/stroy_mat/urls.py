from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('has_app.urls')),
    url(r'^/chat/$', include("django_socketio.urls")),
    url(r'^/chat/$', include("chat.urls")),
]
