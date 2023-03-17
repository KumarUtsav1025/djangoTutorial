from django.urls import path
from home.views import index, person

urlpatterns = [
    path('', index),
    path('/person', person)
]