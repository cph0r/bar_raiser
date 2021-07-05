from django.urls import path

from . import views


app_name = 'video_app'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('view',views.view,name='view'),
    path('search/<str:q>',views.search,name='search')
]