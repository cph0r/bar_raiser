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
    start = request.POST.get(START)
    end = request.POST.get(END)
    procuct_id = request.POST.get(PRODUCT_ID)
    max_deals = request.POST.get(MAX)

    if start and end and procuct_id and max_deals:
        start = datetime.datetime.strptime(start, '%YYYY-%m-%d')
        end = datetime.datetime.strptime(end, '%YYYY-%m-%d')
        entry_map = {
            START :start,
            END:end,
            PRODUCT_ID:int(procuct_id),
            MAX_DEALS :int(max_deals),
            CURRENT_DEALS :0
        }
        getattr(models,STATUS).objects.update_or_create(**entry_map)
        return JsonResponse({'Deal Created':''})
    else:
        return JsonResponse({'error':'incomplete data'})


@api_view([POST])
def update(request):
    deal_id = request.POST.get(DEAL_ID) 
    start = request.POST.get(START)
    end = request.POST.get(END)
    procuct_id = request.POST.get(END)
    max_deals = request.POST.get(MAX)

    if deal_id and start and end and procuct_id and max_deals:
        entry_map = {
            START :start,
            END:end,
            PRODUCT_ID:int(procuct_id),
            MAX_DEALS :int(max_deals),
            CURRENT_DEALS :0
        }
        getattr(models,STATUS).objects.update_or_create(deal_id=int(deal_id),defaults=entry_map)
        return JsonResponse({'Deal Updated':deal_id})
    else:
        return JsonResponse({'error':'incomplete data'})


@api_view([POST])
def delete(request):
    deal_id =  request.POST.get(DEAL_ID)
    if deal_id:
        a,b = getattr(models,DEALS).objects.update_or_create(id=deal_id,default={STATUS_ID:2})
        return JsonResponse({'Success':'deal deleted'})
    else:
        return JsonResponse({'error':'incomplete data'})


@api_view([GET])
def claim(request):
    """API"""
    user_id = request.POST.get(USER_ID)
    t = datetime.datetime.now()
    deal_id =  request.POST.get(PRODUCT_ID)
    if user_id and t and deal_id:
        try:
            entry = getattr(models,DEALS).objects.get(id=deal_id)
            if entry.current_deals == entry.max_deals:
                return JsonResponse({'error: ':'deal limit exceded'})
            else:
                if t <= entry.end and entry.status_id == 1:
                    getattr(models,DEALS).objects.update_or_create(id=deal_id,default={CURRENT_DEALS:entry.current__deals+1})
                    return JsonResponse({'success: ':'deal claimed'})
                else:
                    return JsonResponse({'error: ':'deal time exceeded'})

        except Exception as ex:
            return JsonResponse({'error: ':'deal doesnt exist'})
    else:
        return JsonResponse({'error':'incomplete data'})
