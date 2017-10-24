from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import upload_file

urlpatterns = [
    url(r'^upload/$', login_required(upload_file), name='upload'),
]
