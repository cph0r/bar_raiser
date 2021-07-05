from django.shortcuts import render

from django.http import HttpResponse

BASE_PATH = 'video_app/base.html'

def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    #  records = getattr(models, BOOK_STORE_TABLE).objects.all();
    return render(request, BASE_PATH, {})