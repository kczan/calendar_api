from datetime import datetime

from django.db.models import Q
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.serializers import (
    CalendarUserSerializer,
    CalendarUserReadSerializer,
    ConferenceRoomSerializer,
    EventSerializer,
    EventReadSerializer,
)
from calendar_event.models import Event
from room.models import ConferenceRoom
from user.models import CalendarUser
from user.permissions import RegistrationPermission, RegistrationAuthentication


class CalendarUserAPIViewset(ModelViewSet):
    queryset = CalendarUser.objects.all().order_by("id")
    filterset_fields = ["company_id"]
    permission_classes = (RegistrationPermission,)
    authentication_classes = [RegistrationAuthentication]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CalendarUserReadSerializer
        return CalendarUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user": user.username}, status=status.HTTP_201_CREATED
        )


class ConferenceRoomAPIViewset(ModelViewSet):
    queryset = ConferenceRoom.objects.all().order_by("id")
    serializer_class = ConferenceRoomSerializer


class EventAPIViewset(ModelViewSet):
    queryset = Event.objects.all().order_by("id")
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["location_id"]
    search_fields = ["$name", "$agenda"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return EventReadSerializer
        return self.serializer_class

    def get_queryset(self):
        user = self.request.user
        qs = self.queryset.filter(
            Q(owner=user) | Q(participants=user) | Q(location__manager=user)
        ).distinct()
        day_str = self.request.query_params.get("day", None)
        if day_str:
            day = datetime.strptime(day_str, "%Y-%m-%d").date()
            return qs.filter(Q(start__date=day) | Q(end__date=day))
        return qs
