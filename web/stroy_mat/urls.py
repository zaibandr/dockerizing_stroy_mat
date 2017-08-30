from django.conf.urls import include, url
from django.contrib import admin
import debug_toolbar

urlpatterns = [
    url(r'^__debug__/', include(debug_toolbar.urls)),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^', include('has_app.urls')),
]
