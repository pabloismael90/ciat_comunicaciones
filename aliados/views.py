# -*- coding: UTF-8 -*-
# 
from django.shortcuts import render_to_response
from django.template import RequestContext
from tagging.models import Tag
from tagging.models import TaggedItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from foros.models import Videos, Audios


# Create your views here.

def todos_videos(request):
	audio = Audios.objects.all()

	paginator = Paginator(audio, 5)

	page = request.GET.get('page')
	try:
		audios = paginator.page(page)
	except PageNotAnInteger:
	    audios = paginator.page(1)
	except EmptyPage:
	    audios = paginator.page(paginator.num_pages)

	return render_to_response('contrapartes/producciones_audios.html', locals(),
		                      context_instance=RequestContext(request))

def todos_audios(request):
	video = Videos.objects.all()

	paginator = Paginator(video, 5)

	page = request.GET.get('page')
	try:
		videos = paginator.page(page)
	except PageNotAnInteger:
		videos = paginator.page(1)
	except EmptyPage:
		videos = paginator.page(paginator.num_pages)

	return render_to_response('contrapartes/producciones_videos.html', locals(),
		                      context_instance = RequestContext(request))