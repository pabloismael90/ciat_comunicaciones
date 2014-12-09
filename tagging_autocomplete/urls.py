from django.conf.urls import *

urlpatterns = patterns('tagging_autocomplete.views',
    url(r'^json$', 'list_tags', name='tagging_autocomplete-list'),
)
