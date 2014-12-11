from django.shortcuts import render
from django.conf import settings

def search(request):
    TEMPLATE = getattr(settings, 'CSE_TEMPLATE', 'django_google_cse/default.html')
    CX_CODE = getattr(settings, 'CX_CODE', '')

    q = request.GET.get('q', '')

    return render(
                request, 
                TEMPLATE, 
                {'q': q, 'CX_CODE': CX_CODE}
            )