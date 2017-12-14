from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from activities.models import Activity
from activities.serializers import ActivitySerializer


class ActivityViewSet(ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer