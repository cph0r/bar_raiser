from django.shortcuts import render

from django.http import HttpResponse
import requests
import json

from requests import models
from requests.api import get
import datetime
from .constants import *
import sched, time
s = sched.scheduler(time.time, time.sleep)

def index(request):
    entries = getattr(models,VIDEOS).objects.all().order('-'+DATE)
    s.enter(60, 1, fill_db, (s,))
    s.run()
    return render(request, BASE_PATH, {ENTRIES:entries})


def fill_db(sc):
    URL = YOUTUBE_BASE_API + API_KEY
    PARAMS = {PART: PART_TYPE, Q: QUERY, MAX_RESULTS: PAGE_THRESHOLD,
              ORDER: DATE, TYPE: VIDEO, PUBLISHED_AFTER: THRESHOLD_DATE}
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    results = data[ITEMS]
    existing_ids  = getattr(models,VIDEOS).objects.all().values_list(VIDEO_ID,flat=True)

    bulk_create_list = []
    for result in results:
        fetched_id = result[ID][VIDEO_ID]
        if fetched_id not in existing_ids:
            timestamp = result[SNIPPET][PUBLISHED_AT]
            timestamp.replace('T',' ').replace('Z','')
            timestamp = datetime.datetime.strptime(timestamp,TIMESTAMP_FORMAT)
            entry = {VIDEO_ID:fetched_id,TITLE:result[SNIPPET][TITLE],
            DESCRIPTION:result[SNIPPET][DESCRIPTION],
            DATE:timestamp,PHOTO:result[SNIPPET][THUMBNAILS][DEFAULT][URL],
            URL:YOUTUBE_BASE_URL+fetched_id}
            new_video_instance = getattr(models,VIDEOS)(**entry)
            bulk_create_list.append(new_video_instance)
    
    created_records = getattr(models,VIDEOS).objects.bulk_create(bulk_create_list)
    print(created_records)
    LAST_MODIFIED = datetime.datime.now()
    print('last modified on :'+ LAST_MODIFIED)
    s.enter(60, 1, fill_db, (sc,))
