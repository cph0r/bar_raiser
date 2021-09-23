from django.shortcuts import redirect, render
import requests
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from .serializers import user_serializer
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

s = sched.scheduler(time.time, time.sleep)

def dashboard(request):
    """Dashboard View"""
    return render(request, BASE_PATH, {})


@api_view([GET])
def view(request):
    """API"""
    entries = None
    paginator = PageNumberPagination()
    results = paginator.paginate_queryset(entries, request)
    serializer = user_serializer(results, many=True)
    return paginator.get_paginated_response(serializer.data)



def run_scheduler():
    """Running fill Db function asynchronously"""
    scheduler = BackgroundScheduler()
    scheduler.configure(timezone='utc')
    # scheduler.add_job(fill_db, 'interval', seconds=10)
    scheduler.start()


