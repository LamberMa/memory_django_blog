from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse


# Create your views here.
def index(request):
    if request.method == 'POST':
        ret = request.FILES.getlist('file')
        print(ret)
        return HttpResponse('...')

    return render(request, 'album/index.html')


def album_upload(request):


    return HttpResponse('...')


def index2(request):
    pass


