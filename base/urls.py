from django.urls import path
from . import views


urlpatterns=[
    path('download/<str:musid>/',views.Main),
]