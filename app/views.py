from django.http.response import JsonResponse
from django.shortcuts import redirect, render
import requests
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from .serializers import user_serializer
import os
import json
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


@api_view([POST])
def create(request):
    body = render_body(request)
    start = body.get(START)
    end = body.get(END)
    product_id = body.get(PRODUCT_ID)
    max_deals = body.get(MAX)
    if start and end and product_id and max_deals:
        try:
            convert_dates(start, end)
            if start > end:
                return JsonResponse({ERROR: DATE_ERROR})
            else:
                entry_map = {
                    START: start,
                    END: end,
                    PRODUCT_ID: int(product_id),
                    MAX_DEALS: int(max_deals),
                    CURRENT_DEALS: 0
                }
                if already_exist(product_id):
                    return JsonResponse({ERROR: DEAL_ALREADY_EXIST})
                else:
                    getattr(models, DEALS).objects.update_or_create(
                        **entry_map)
                    return JsonResponse({CREATED: ''})
        except:
            return JsonResponse({ERROR: FORMAT_ERROR})

    else:
        return JsonResponse({ERROR: INCOMPLETE_DATA})



@api_view([POST])
def update(request):
    body = render_body(request)
    start = body.get(START)
    end = body.get(END)
    product_id = body.get(PRODUCT_ID)
    max_deals = body.get(MAX)
    deal_id = body.get(DEAL_ID)
    
    if deal_id and start and end and product_id and max_deals:
        try:
            convert_dates(start, end)
            if start > end:
                return JsonResponse({ERROR: DATE_ERROR})
            else:
                entry_map = {
                    START: start,
                    END: end,
                    PRODUCT_ID: int(product_id),
                    MAX_DEALS: int(max_deals),
                    CURRENT_DEALS: 0
                }
                a = getattr(models, DEALS).objects.filter(deal_id=int(deal_id),status=1)
                if len(a) == 0:
                    return JsonResponse({ERROR: DEAL_DOESNT_EXIST})
                else:
                    getattr(models, STATUS).objects.update_or_create(
                    deal_id=int(deal_id),status=1, defaults=entry_map)
                    return JsonResponse({UPDATED: deal_id})
        except:
            return JsonResponse({ERROR: FORMAT_ERROR})
    else:
        return JsonResponse({ERROR: INCOMPLETE_DATA})



@api_view([POST])
def delete(request):
    body = render_body(request)
    deal_id = body.get(DEAL_ID)
    if deal_id:
        try:
            getattr(models, DEALS).objects.get(deal_id=int(deal_id),status=1)
            getattr(models, DEALS).objects.update_or_create(id=deal_id, default={STATUS_ID: 2})
            return JsonResponse({SUCCESS: DELETED})
        except:
            return JsonResponse({ERROR: DEAL_DOESNT_EXIST})
    else:
        return JsonResponse({ERROR:INCOMPLETE_DATA})


@api_view([GET])
def claim(request):
    """API"""
    body = render_body(request)
    user_id = body.get(USER_ID)
    t = datetime.datetime.now()
    deal_id = body.get(PRODUCT_ID)
    if user_id and t and deal_id:
        try:
            entry = getattr(models, DEALS).objects.get(id=deal_id)
            if entry.current_deals == entry.max_deals:
                return JsonResponse({ERROR: LIMIT_EXCEDED})
            else:
                if t <= entry.end and entry.status_id == 1:
                    getattr(models, DEALS).objects.update_or_create(
                        id=deal_id, default={CURRENT_DEALS: entry.current__deals+1})
                    return JsonResponse({SUCCESS: DEAL_CLAIMED})
                else:
                    return JsonResponse({ERROR: TIME_EXCEDED})
        except Exception as ex:
            return JsonResponse({ERROR: DEAL_DOESNT_EXIST})
    else:
        return JsonResponse({ERROR: INCOMPLETE_DATA})


def render_body(request):
    body_unicode = request.body.decode(UTF_8)
    body = json.loads(body_unicode)
    return body


def convert_dates(start, end):
    start = datetime.datetime.strptime(start, YMD_HMS)
    end = datetime.datetime.strptime(end, YMD_HMS)

def already_exist(product_id):
    a = getattr(models, DEALS).objects.filter(product_id=int(product_id),status=1)
    if len(a) > 0:
        return True
    else:
        return False