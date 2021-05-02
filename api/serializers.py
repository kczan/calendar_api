import datetime
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault

from calendar_event.models import Event
from room.models import ConferenceRoom
from user.models import CalendarUser

SECONDS_IN_HOUR = 60 * 60


class CalendarUserSerializer(ModelSerializer):
    class Meta:
        model = CalendarUser
        fields = '__all__'


class CalendarUserReadSerializer(ModelSerializer):
    class Meta:
        model = CalendarUser
        fields = ['id', 'first_name', 'last_name', 'username', 'email']


class ConferenceRoomSerializer(ModelSerializer):
    class Meta:
        model = ConferenceRoom
        fields = '__all__'

class EventReadSerializer(ModelSerializer):
    location = ConferenceRoomSerializer()
    class Meta:
        model = Event
        fields = '__all__'


class EventSerializer(ModelSerializer):
    owner = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Event
        fields = '__all__'

    def validate(self, data):
        start_datetime = data['start']
        end_datetime = data['end']
        if end_datetime < start_datetime:
            raise ValidationError({'detail': 'A meeting has to end only after starting.'})
        duration = end_datetime - start_datetime
        if duration.seconds > 8 * SECONDS_IN_HOUR:
            raise ValidationError({'detail': 'A meeting cannot last longer than 8 hours.'})
        return data
