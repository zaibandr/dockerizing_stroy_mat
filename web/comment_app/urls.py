from django.conf.urls import url

from .views import EditComment

urlpatterns = [
    url(r'^edit_comment/(?P<pk>[0-9]+)/$', EditComment.as_view(), name='edit_comment'),
]
