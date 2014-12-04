from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^$', 'django_google_cse.views.search', name="django_google_cse"),
)