from configurations.settings import CACHE_TTL
from rest_framework import decorators
from video_app.documents import video_document
from django.shortcuts import redirect, render
import requests
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from .serializers import videos_serializer
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler

from . import models
import datetime
from .constants import *
import sched
import time
from django.db.models import Q
from django.contrib import messages
from django.utils.timezone import make_aware
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import FilteringFilterBackend, CompoundSearchFilterBackend,OrderingFilterBackend
from .documents import *
from django.core.cache import cache
from django.conf  import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
s = sched.scheduler(time.time, time.sleep)

CACHE_TTL = getattr(settings,'CACHE_TTL',DEFAULT_TIMEOUT)
def dashboard(request):
    """Dashboard View to display locally stored results in decreasing order of Published Date"""
    entries = getattr(models, VIDEOS).objects.all().order_by('-'+DATE)
    return render(request, BASE_PATH, {ENTRIES: entries})


@api_view([GET])
def view(request):
    """API for Viewing"""
    # Applied redis caching for optimization
    # if cache.get(VIDEOS):
    #     entries = cache.get(VIDEOS)
    # else:
    entries = getattr(models, VIDEOS).objects.all().order_by('-'+DATE)
    # cache.set(VIDEOS,entries)
    paginator = PageNumberPagination()
    results = paginator.paginate_queryset(entries, request)
    serializer = videos_serializer(results, many=True)
    return paginator.get_paginated_response(serializer.data)

# OPTIMISED SEARCH WITH ELASTIC SEARCH AND SHARDING, UNCOMMENT FOR USE WITH ELASTIC SEARCH
# class search(DocumentViewSet):
#     document = video_document
#     serializer_class = videos_serializer 
#     filter_backends = [FilteringFilterBackend,CompoundSearchFilterBackend,OrderingFilterBackend]
#     search_fields = (TITLE,DESCRIPTION)
#     multi_search_fields = [TITLE,DESCRIPTION]
#     filter_fields = {TITLE:TITLE,DESCRIPTION:DESCRIPTION}
#     ordering_fields = {}
#     ordering = ('-date')

# NORMAL SEARCH TO BE USED IN CASE ELASTIC SEARCH IS NOT RUNNING ON SERVER 
@api_view([GET])
def search(request):
    """API for Searching"""
    paginator = PageNumberPagination()
    query_parameters = request.GET.get('search').split()
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
    # entries = video_document.search().filter('match',title=request.GET.get('search'),description=request.GET.get('search'))
    results = paginator.paginate_queryset(entries, request)
    serializer = videos_serializer(results, many=True)
    return paginator.get_paginated_response(serializer.data)


def fill_db():
    """Create Video entries in db"""
    # fetch all api keys
    api_keys = getattr(models, API_KEYS).objects.all(
    ).values_list(API_KEY, flat=True)
    success = False

    # iterate over API keys till successfull api call
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
    """Save Results in the local DB"""
    existing_ids = getattr(models, VIDEOS).objects.all(
    ).values_list(VIDEO_ID, flat=True)
    fetched_ids = create_new_entries(results, existing_ids)
    delete_entries(existing_ids, fetched_ids)
    LAST_MODIFIED = datetime.datetime.now()
    print(LAST_MODIFIED_ON + str(LAST_MODIFIED))


def delete_entries(existing_ids, fetched_ids):
    """Delete Videos that are no longer present in search Result"""
    to_delete_ids = []
    for entry in existing_ids:
        if entry not in fetched_ids:
            to_delete_ids.append(entry)

    if len(to_delete_ids) != 0:
        getattr(models, VIDEOS).objects.filter(
            **{VIDEO_ID+'__in': to_delete_ids}).delete()


def create_new_entries(results, existing_ids):
    """Create New Videos Entries"""
    fetched_ids = []
    bulk_create_list = []
    for result in results:
        fetched_id = result[ID]['videoId']
        fetched_ids.append(fetched_id)
        if fetched_id not in existing_ids:
            timestamp = result[SNIPPET][PUBLISHED_AT]
            timestamp = timestamp.replace(
                'T', ' ').replace('Z', '')
            timestamp = make_aware(datetime.datetime.strptime(
                timestamp, TIMESTAMP_FORMAT))
            entry = {VIDEO_ID: fetched_id, TITLE: result[SNIPPET][TITLE],
                     DESCRIPTION: result[SNIPPET][DESCRIPTION],
                     DATE: timestamp, PHOTO: result[SNIPPET][THUMBNAILS][DEFAULT][URL],
                     URL: YOUTUBE_BASE_URL+fetched_id}
            new_video_instance = getattr(models, VIDEOS)(**entry)
            bulk_create_list.append(new_video_instance)

    getattr(models, VIDEOS).objects.bulk_create(bulk_create_list)
    return fetched_ids


def fetch_results(api_key):
    """Fetch results from youtube api"""
    api_url = YOUTUBE_BASE_API + api_key
    PARAMS = {PART: PART_TYPE, QU: QUERY, MAX_RESULTS: PAGE_THRESHOLD,
              ORDER: DATE, TYPE: VIDEO, PUBLISHED_AFTER: THRESHOLD_DATE}
    r = requests.get(url=api_url, params=PARAMS)
    data = r.json()
    results = data[ITEMS]
    return results


def add(request):
    if request.method == POST:
        # Save Api Keys with unique names
        try:
            name = request.POST.get(NAME)
            key = request.POST.get(API_KEY)

            if name == BLANK or name == None or key == BLANK or key == None:
                # Handle Blank or null names and keys
                messages.error(request, BLANK_MESSAGE)
                return redirect(DASHBOARD)
            else:
                # Handle Duplicity of name and key
                getattr(models, API_KEYS).objects.get(
                    **{NAME+IEXACT: name, API_KEY+IEXACT: key})
                messages.error(request, DUPLICATE)
                return redirect(DASHBOARD)
                
        except Exception as ex:
            print(ex)
            # Saving Api keys in db
            getattr(models, API_KEYS).objects.update_or_create(
                **{NAME: name, API_KEY: key})
            messages.success(request, SUCCESS)
            return redirect(DASHBOARD)
    else:
        # Render Modal in Front end
        entries = getattr(models, API_KEYS).objects.all()
        return render(request, MODAL_PATH, {ENTRIES: entries})


def run_scheduler():
    """Running fill Db function asynchronously"""
    scheduler = BackgroundScheduler()
    scheduler.configure(timezone='utc')
    scheduler.add_job(fill_db, 'interval', seconds=10)
    scheduler.start()


if os.environ.get('HEROKU') == None:
    """Checking for env variable to check if sever is deployed in heroku"""
    print('Not in heroku, Api call will work')
    run_scheduler()
else:
    print('Inside heroku server, API call are restricted to prevent quota Exhaustion')
