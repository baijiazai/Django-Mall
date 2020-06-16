from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from demo.models import Upload


def index(request):
    return HttpResponse('hello demo')


def upload(request):
    if request.method == 'POST':
        img = request.FILES.get('img')
        Upload.objects.create(img=img)
        return HttpResponseRedirect(reverse('demo:upload'))
    images = Upload.objects.all()
    return render(request, 'demo/upload.html', {'images': images})
