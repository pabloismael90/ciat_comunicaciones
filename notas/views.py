# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from models import *
from agendas.models import *
from contrapartes.models import *
from forms import *
from django.contrib.contenttypes.generic import generic_inlineformset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import thread
import datetime
import operator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.views.generic import TemplateView
from foros.models import Documentos, Videos

# Create your views here.

def logout_page(request):
  logout(request)
  return HttpResponseRedirect('/')

class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['book_list'] = "hola!"
        return context

def lista_notas(request):
    notas_list = Notas.objects.all().order_by('-fecha','-id')
    agenda = Agendas.objects.all().order_by('-inicio','-id')[1:4]
    paises = Pais.objects.all()

    paginator = Paginator(notas_list, 4)

    page = request.GET.get('page')
    try:
        notas = paginator.page(page)
    except PageNotAnInteger:
        notas = paginator.page(1)
    except EmptyPage:
        notas = paginator.page(paginator.num_pages)

    return render_to_response('notas/notas_list.html', locals(),
                              context_instance=RequestContext(request))

def detalle_notas(request, id):
    nota = get_object_or_404(Notas, id=id)
    agenda = Agendas.objects.all().order_by('-inicio','-id')[1:4]

    if request.method == 'POST':
        form = ComentarioForm(request.POST)

        if form.is_valid():
            form_uncommited = form.save(commit=False)
            form_uncommited.user = request.user
            form_uncommited.nota = nota
            form_uncommited.save()

        return HttpResponseRedirect('/notas/%d/#cmt%d' % (nota.id,form.instance.id) )

    else:
        form = ComentarioForm()

    return render_to_response('notas/notas_detail.html', locals(),
                                 context_instance=RequestContext(request))  

def lista_notas_pais(request,id):
    notas_list = Notas.objects.filter(user__userprofile__contraparte__pais__id=id).order_by('-fecha','-id')
    paises = Pais.objects.all()
    pais_selecto = Pais.objects.get(pk=id)

    paginator = Paginator(notas_list, 4)

    page = request.GET.get('page')
    try:
        notas = paginator.page(page)
    except PageNotAnInteger:
        notas = paginator.page(1)
    except EmptyPage:
        notas = paginator.page(paginator.num_pages)

    return render_to_response('notas/notas_list.html', locals(),
                              context_instance=RequestContext(request))


def index(request):
    notasslide = Notas.objects.all().order_by('-fecha','-id')
    evento = Agendas.objects.filter(publico=True).order_by('-inicio')[:3]
    paises = Pais.objects.all()
    contrapartes = Contraparte.objects.filter(tipo=1)
    audio = Audios.objects.order_by('-id')[:1]
    documentos = Documentos.objects.order_by('-id')[:2]
    video = Videos.objects.order_by('-id')[:1]

    return render_to_response('index.html', locals(),
                              context_instance=RequestContext(request))

@login_required
def crear_nota(request):
    if request.method == 'POST':
        form = NotasForms(request.POST)
        form2 = FotoForm(request.POST, request.FILES)
        form3 = AdjuntoForm(request.POST, request.FILES)
        form4 = VideoForm(request.POST)
        form5 = AudioForm(request.POST, request.FILES)

    	if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid():
            form_uncommited = form.save(commit=False)
            form_uncommited.user = request.user
            form_uncommited.save()
            if form2.cleaned_data['nombre_img'] != '':
                form2_uncommited = form2.save(commit=False)
                form2_uncommited.content_object = form_uncommited
                form2_uncommited.save()
            if form3.cleaned_data['nombre_doc'] != '':    
                form3_uncommited = form3.save(commit=False)
                form3_uncommited.content_object = form_uncommited
                form3_uncommited.save()
            if form4.cleaned_data['nombre_video'] != '':
                form4_uncommitd = form4.save(commit=False)
                form4_uncommitd.content_object = form_uncommited
                form4_uncommitd.save()
            if form5.cleaned_data['nombre_audio'] != '':
                form5_uncommitd = form5.save(commit=False)
                form5_uncommitd.content_object = form_uncommited
                form5_uncommitd.save()

            thread.start_new_thread(notify_all_notas, (form_uncommited,))
            return HttpResponseRedirect('/foros/privado/nota/')
    else:
        form = NotasForms()
        form2 = FotoForm()
        form3 = AdjuntoForm()
        form4 = VideoForm()
        form5 = AudioForm()
    return render_to_response('notas/crear_nota.html', locals(),
    	                         context_instance=RequestContext(request))

@login_required
def editar_nota(request, id):
    nota = get_object_or_404(Notas, id=id)
    NotaFormSet = generic_inlineformset_factory(Imagen, extra=5, max_num=5)
    Nota2FormSet = generic_inlineformset_factory(Documentos, extra=5, max_num=5)
    NotavideoFormSet = generic_inlineformset_factory(Videos, extra=5, max_num=5)
    NotaAudioFormSet = generic_inlineformset_factory(Audios, extra=5, max_num=5)
    form2 = NotaFormSet(instance=nota)
    form3 = Nota2FormSet(instance=nota)
    form4 = NotavideoFormSet(instance=nota)
    form5 = NotaAudioFormSet(instance=nota)

    if not nota.user == request.user and not request.user.is_superuser:
    	return HttpResponse("Usted no puede editar esta nota")

    if request.method == 'POST':
        form = NotasForms(request.POST, instance=nota)
        form2 = NotaFormSet(data=request.POST, files=request.FILES, instance=nota)
        form3 = Nota2FormSet(data=request.POST, files=request.FILES, instance=nota)
        form4 = NotavideoFormSet(data=request.POST, files=request.FILES, instance=nota)
        form5 = NotaAudioFormSet(data=request.POST, files=request.FILES, instance=nota)
    	if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid():
            nota.titulo = request.POST['titulo']
            nota.contenido = request.POST['contenido']
            nota.fecha = datetime.datetime.now()
            nota.user = request.user
            nota.save()
            #salvando inline
            form2.save()
            form3.save()
            form4.save()
            form5.save()
            return HttpResponseRedirect('%s?shva=ok' % nota.get_absolute_url())
    else:
        form = NotasForms(instance=nota)
        form2 = NotaFormSet(instance=nota)
        form3 = Nota2FormSet(instance=nota)
        form4 = NotavideoFormSet(instance=nota)
        form5 = NotaAudioFormSet(instance=nota)


    return render_to_response('notas/editar_nota.html', locals(),
    	                         context_instance=RequestContext(request))

@login_required
def borrar_nota(request, id):
    nota = get_object_or_404(Notas, pk=id)

    if nota.user == request.user or request.user.is_superuser:
        nota.delete()
        #return redirect('/notas')
        return HttpResponseRedirect('/notas/?shva=erase')
    else:
        return redirect('/')

def notify_all_notas(notas):
    site = Site.objects.get_current()
    users = User.objects.all() #.exclude(username=foros.contraparte.username)
    contenido = render_to_string('notas/notify_new_nota.txt', {'nota': notas,
                                 'url': '%s/notas/%s' % (site, notas.id),
                                 #'url_aporte': '%s/foros/ver/%s/#aporte' % (site, foros.id),
                                 })
    send_mail('Nueva Nota en AMARC', contenido, 'amarc@amarcnicaragua.org', [user.email for user in users if user.email])

@login_required
def comentar_nota(request, id):
    nota = get_object_or_404(Notas, id=id)

    if request.method == 'POST':
        form = ComentarioForm(request.POST)

        if form.is_valid():
            form_uncommited = form.save(commit=False)
            form_uncommited.user = request.user
            form_uncommited.nota = nota
            form_uncommited.save()

        return HttpResponseRedirect('/notas/ver/%d' % nota.id)

    else:
        form = ComentarioForm()

    return render_to_response('privados/ver_nota.html', locals(),
                                 context_instance=RequestContext(request))  
