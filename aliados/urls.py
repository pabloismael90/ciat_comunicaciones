from django.conf.urls.defaults import *
from django.views.generic import ListView, DetailView
from .models import Aliados

urlpatterns = patterns('aliados.views',
    url(r'^$', ListView.as_view(model=Aliados, 
    	                        template_name="aliados/aliado_list.html"),
                                name="aliados-list"),
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(model=Aliados, 
     	                                      template_name='aliados/aliado_detail.html'),
                                              name='aliados-detail'),
    url(r'^videos/$', 'todos_videos', name='todos-videos'),
    url(r'^audios/$', 'todos_audios', name='todos-audios'),
)