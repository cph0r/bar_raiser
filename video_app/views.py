from django.shortcuts import redirect, render
from django.http import HttpResponse
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import videos_serializer
# import grequests
# import asyncio
import time
from apscheduler.schedulers.background import BackgroundScheduler

from . import models
from requests.api import get
import datetime
from .constants import *
import sched
import time
from django.db.models import Q
from django.contrib import messages

from video_app import serializers
s = sched.scheduler(time.time, time.sleep)


def dashboard(request):
    entries = getattr(models, VIDEOS).objects.all().order_by('-'+DATE)
    scheduler = BackgroundScheduler()
    scheduler.configure(timezone='utc')
    scheduler.add_job(fill_db, 'interval', seconds=10)
    # scheduler.add
    scheduler.start()
    return render(request, BASE_PATH, {ENTRIES: entries})


@api_view([GET])
def view(request):
    entries = getattr(models, VIDEOS).objects.all().order_by('-'+DATE)
    serializer = videos_serializer(entries, many=True)
    return Response(serializer.data)


@api_view([GET])
def search(request, q):
    query_parameters = q.split()
    q1 = Q()
    q2 = Q()
    q3 = Q()
    q4 = Q()

    for entry in query_parameters:
        q1 &= Q(**{TITLE+ICONTAINS: entry})
        q2 &= Q(**{DESCRIPTION+ICONTAINS: entry})
        q3 |= Q(**{TITLE+ICONTAINS: entry})
        q4 |= Q(**{DESCRIPTION+ICONTAINS: entry})
    final_query = q1 | q2 | q3 | q4
    entries = getattr(models, VIDEOS).objects.filter(
        final_query).order_by('-'+DATE)
    serializer = videos_serializer(entries, many=True)
    return Response(serializer.data)

def fill_db():
    api_keys = getattr(models, API_KEYS).objects.all(
    ).values_list(API_KEY, flat=True)
    success = False
    for api_key in api_keys:
        if success == False:
            try:
                results = fetch_results(api_key)
                save_results(results)
                success = True
            except Exception as ex:
                print(ex)
                print(LIMIT_EXHAUSTED + api_key)
                success = False
        else:
            print(FETCHED_RESULT)
            break

def save_results(results):
    existing_ids = getattr(models, VIDEOS).objects.all(
                ).values_list(VIDEO_ID, flat=True)
    fetched_ids = create_new_entries(results, existing_ids)
    delete_entries(existing_ids, fetched_ids)
    
    LAST_MODIFIED = datetime.datetime.now()
    print(LAST_MODIFIED_ON + str(LAST_MODIFIED))

def delete_entries(existing_ids, fetched_ids):
    to_delete_ids = []
    for entry in existing_ids:
        if entry not in fetched_ids:
            to_delete_ids.append(entry)
    
    if len(to_delete_ids) != 0:
        getattr(models, VIDEOS).objects.filter(**{VIDEO_ID+'__in':to_delete_ids}).delete()

def create_new_entries(results, existing_ids):
    fetched_ids = []
    bulk_create_list = []
    for result in results:
        fetched_id = result[ID]['videoId']
        fetched_ids.append(fetched_id)
        if fetched_id not in existing_ids:
            timestamp = result[SNIPPET][PUBLISHED_AT]
            timestamp = timestamp.replace(
                            'T', ' ').replace('Z', '')
            timestamp = datetime.datetime.strptime(
                            timestamp, TIMESTAMP_FORMAT)
            entry = {VIDEO_ID: fetched_id, TITLE: result[SNIPPET][TITLE],
                                 DESCRIPTION: result[SNIPPET][DESCRIPTION],
                                 DATE: timestamp, PHOTO: result[SNIPPET][THUMBNAILS][DEFAULT][URL],
                                 URL: YOUTUBE_BASE_URL+fetched_id}
            new_video_instance = getattr(models, VIDEOS)(**entry)
            bulk_create_list.append(new_video_instance)

    getattr(models, VIDEOS).objects.bulk_create(bulk_create_list)
    return fetched_ids

def fetch_results(api_key):
    api_url = YOUTUBE_BASE_API + api_key
    PARAMS = {PART: PART_TYPE, QU: QUERY, MAX_RESULTS: PAGE_THRESHOLD,
                          ORDER: DATE, TYPE: VIDEO, PUBLISHED_AFTER: THRESHOLD_DATE}
    r = requests.get(url=api_url, params=PARAMS)
    data = r.json()
    results = data[ITEMS]
    return results


def add(request):
    if request.method == POST:
        try:
            name = request.POST.get(NAME)
            key = request.POST.get(API_KEY)
            if name == BLANK or name == None or key == BLANK or key == None:
                messages.error(request, BLANK_MESSAGE)
                return redirect(DASHBOARD)
            else:
                record = getattr(models, API_KEYS).objects.get(
                    **{NAME+IEXACT: name, API_KEY+IEXACT: key})
                messages.error(request, DUPLICATE)
                return redirect(DASHBOARD)
        except Exception as ex:
            print(ex)
            getattr(models, API_KEYS).objects.update_or_create(
                **{NAME: name, API_KEY: key})
            messages.success(request, SUCCESS)
            return redirect(DASHBOARD)
    else:
        entries = getattr(models, API_KEYS).objects.all()
        return render(request, MODAL_PATH, {ENTRIES: entries})

