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
            name = self.request.query_params.get('name')
            description = self.request.query_params.get('description')
            start_time = self.request.query_params.get('start_time')
            end_time = self.request.query_params.get('end_time')
            productive = self.request.query_params.get('productive')
            category = self.request.query_params.get('category')
            
            activities = Activity.objects.filter(user=self.request.user)

            if name:
                activities = activities.filter(name__icontains=name)

            if description:
                activities = activities.filter(description__icontains=description)

            if start_time:
                activities = activities.filter(start_time__icontains=start_time)

            if end_time:
                activities = activities.filter(end_time__icontains=end_time)

            if productive:
                activities = activities.filter(productive=productive)

            if category:
                activities = activities.filter(category__name=category)

            return activities
        except TypeError:
            raise exceptions.NotAuthenticated()
