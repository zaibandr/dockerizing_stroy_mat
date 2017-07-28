from django.conf.urls import include, url
from django.contrib import admin

from django_private_chat import urls as django_private_chat_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('has_app.urls')),
    url(r'^chat/', include(django_private_chat_urls)),
]
