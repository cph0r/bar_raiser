from django.shortcuts import redirect, render
from django.http import HttpResponse
import requests
# from grequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import videos_serializer

from . import models
from requests.api import get
import datetime
from .constants import *
import sched, time
from django.db.models import Q
from django.contrib import messages

from video_app import serializers
s = sched.scheduler(time.time, time.sleep)

def dashboard(request):
    entries = getattr(models,VIDEOS).objects.all().order_by('-'+DATE)
    # s.enter(60, 1, fill_db, (s,))
    # s.run()
    return render(request, BASE_PATH, {ENTRIES:entries})


@api_view(['GET'])
def view(request):
    entries = getattr(models,VIDEOS).objects.all().order_by('-'+DATE)
    serializer = videos_serializer(entries,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search(request,q):
    query_parameters = q.split()
    q1 = Q()
    q2 = Q()
    q3 = Q()
    q4 = Q()

    for entry in query_parameters:
        q1 &= Q(**{TITLE+ICONTAINS:entry})
        q2 &= Q(**{DESCRIPTION+ICONTAINS:entry})
        q3 |= Q(**{TITLE+ICONTAINS:entry})
        q4 |= Q(**{DESCRIPTION+ICONTAINS:entry})
    final_query = q1 | q2 | q3 | q4
    entries = getattr(models,VIDEOS).objects.filter(final_query).order_by('-'+DATE)
    serializer = videos_serializer(entries,many=True)
    return Response(serializer.data)


def fill_db(sc):
    api_url = YOUTUBE_BASE_API + API_KEY
    PARAMS = {PART: PART_TYPE, QU: QUERY, MAX_RESULTS: PAGE_THRESHOLD,
              ORDER: DATE, TYPE: VIDEO, PUBLISHED_AFTER: THRESHOLD_DATE}
    r = requests.get(url=api_url, params=PARAMS)
    data = r.json()
    results = data[ITEMS]
    existing_ids  = getattr(models,VIDEOS).objects.all().values_list(VIDEO_ID,flat=True)

    bulk_create_list = []
    for result in results:
        fetched_id = result[ID]['videoId']
        if fetched_id not in existing_ids:
            timestamp = result[SNIPPET][PUBLISHED_AT]
            timestamp = timestamp.replace('T',' ').replace('Z','')
            timestamp = datetime.datetime.strptime(timestamp,TIMESTAMP_FORMAT)
            entry = {VIDEO_ID:fetched_id,TITLE:result[SNIPPET][TITLE],
            DESCRIPTION:result[SNIPPET][DESCRIPTION],
            DATE:timestamp,PHOTO:result[SNIPPET][THUMBNAILS][DEFAULT][URL],
            URL:YOUTUBE_BASE_URL+fetched_id}
            new_video_instance = getattr(models,VIDEOS)(**entry)
            bulk_create_list.append(new_video_instance)
    
    created_records = getattr(models,VIDEOS).objects.bulk_create(bulk_create_list)
    print(created_records)
    LAST_MODIFIED = datetime.datetime.now()
    print('Last modified on :'+ str(LAST_MODIFIED))
    s.enter(60, 1, fill_db, (sc,))


def add(request):
    if request.method == 'POST':
        try:
            name = request.POST.get(NAME)
            key = request.POST.get('api_key')
            if name == '' or name == None or key == '' or key == None:
                messages.error(request,'Blank name or key')
                return redirect('video_app:dashboard')
            else:
                record = getattr(models,'api_keys').objects.get(**{NAME+IEXACT:name,'api_key'+IEXACT:key})
                messages.error(request,'Duplicate name or key')
                return redirect('video_app:dashboard')
        except Exception as ex:
            print(ex)
            record,created = getattr(models,'api_keys').objects.update_or_create(**{NAME:name,'api_key':key})
            print(record,created)
            messages.success(request,'Added Successfully')    
            return redirect('video_app:dashboard')
    else:
        entries = getattr(models,'api_keys').objects.all()
        return render(request,MODAL_PATH,{ENTRIES:entries})
