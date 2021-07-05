from django.shortcuts import render

from django.http import HttpResponse
import requests
import json

from requests import models

BASE_PATH = 'video_app/base.html'


def index(request):
    api_key = 'AIzaSyBXXzS77zT4P-5U15_uhAD_9nT6vQCL8QM'
    published_after = '2020-01-01T18:42:16Z'
    URL = "https://youtube.googleapis.com/youtube/v3/search?key=" + api_key
    PARAMS = {'part': 'snippet', 'q': 'cricket', 'maxResults': '5',
              'order': 'date', 'type': 'video', 'publishedAfter': published_after}
    r = requests.get(url=URL, params=PARAMS)
    # data = json.loads(r.text)
    data = r.json()
    results = data['items']
    # print(results)
    for result in results:
        print(result['id']['videoId'])
        print(result['snippet']['title'])
        print(result['snippet']['description'])
        print(result['snippet']['publishedAt'])
        print(result['snippet']['thumbnails']['default']['url'])
    return render(request, BASE_PATH, {})


def fill_db():
    api_key = 'AIzaSyBXXzS77zT4P-5U15_uhAD_9nT6vQCL8QM'
    published_after = '2020-01-01T18:42:16Z'
    URL = "https://youtube.googleapis.com/youtube/v3/search?key=" + api_key
    PARAMS = {'part': 'snippet', 'q': 'cricket', 'maxResults': '5',
              'order': 'date', 'type': 'video', 'publishedAfter': published_after}
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    results = data['items']
    videos = getattr(models,'videos').objects.all()
    for result in results:
        print(result['id']['videoId'])
        print(result['snippet']['title'])
        print(result['snippet']['description'])
        print(result['snippet']['publishedAt'])
        print(result['snippet']['thumbnails']['default']['url'])

