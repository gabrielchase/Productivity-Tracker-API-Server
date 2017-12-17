from django.shortcuts import render

from rest_framework import permissions, exceptions
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from activities.models import Activity
from activities.serializers import ActivitySerializer
from activities.permissions import ActivityPermission


class ActivityViewSet(ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (ActivityPermission,)

    def get_queryset(self):
        try:
            return Activity.objects.filter(user=self.request.user)
        except TypeError:
            raise exceptions.NotAuthenticated()
