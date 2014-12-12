from django.conf.urls import *
from django.views.generic import ListView, DetailView
from models import Contraparte

urlpatterns = patterns('contrapartes.views',
    url(r'^$', 'lista_contrapartes', name="contraparte-list"),
    url(r'^pais/(?P<id>\d+)/$', 'lista_contrapartes_pais', name="contraparte_list_pais"),
    url(r'^mapa/$', 'lista_contrapartes_mapa', name="contraparte-list-mapa"),
    url(r'^(?P<id>\d+)/$', 'detalle_contraparte', name="detalle-contraparte"),
    # url(r'^(?P<pk>\d+)/$', DetailView.as_view(model=Contraparte, 
    # 	                                        template_name='notas/contraparte_detail.html'),
    #                                             name='contraparte-detail'),
    url(r'^crear/$', 'crear_contraparte', name="crear-contraparte"),
    url(r'^editar/(?P<id>\d+)/$', 'editar_contraparte', name='editar-contraparte'),
    # url(r'^borrar/(?P<id>\d+)/$', 'borrar_contraparte', name='borrar-contraparte'),
    url(r'^usuario/editar/$', 'editar_usuario_perfil', name='editar-usuario-perfil'),
    url(r'^mensaje/ver/$', 'enviar_mensaje', name="enviar-mensaje"),
    url(r'^estadisticas/ver/$', 'estadisticas', name="estadisticas"),
    url(r'^ver_mapa_completo/$', 'datos_mapa', name="datos-mapa"),
    url(r'^videos/$', 'todos_videos', name='todos_videos'),
    url(r'^audios/$', 'todos_audios', name='todos_audios'),
    url(r'^lista/$', 'lista_aliados', name='todos-lista-aliados'),
    url(r'^detalle/(?P<id>\d+)/$', 'detalle_aliados', name='aliados'),
    url(r'^radio_audio/(?P<id>\d+)/$', 'audios_radios', name='audios_radios'),
    
    )