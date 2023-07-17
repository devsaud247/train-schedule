from rest_framework import serializers

from .models import TrainSchedule


class TrainScheduleSerializer(serializers.ModelSerializer):
    """
    Serializer for the TrainSchedule model.

    Attributes:
        id (int): The ID of the train schedule.
        name (str): The name of the train line.
        schedule (str): The schedule of train arrivals at the station.
    """

    class Meta:
        model = TrainSchedule
        fields = ("id", "name", "schedule")
