from datetime import datetime

from rest_framework import generics
from rest_framework.response import Response

from .helpers import (
    find_next_day_simultaneous_time,
    find_next_simultaneous_time,
    get_station_schedule,
)
from .models import TrainSchedule
from .serializers import TrainScheduleSerializer


class TrainScheduleListCreateView(generics.ListCreateAPIView):
    """API view for creating and retrieving train schedules."""

    queryset = TrainSchedule.objects.all()
    serializer_class = TrainScheduleSerializer


class NextSimultaneousTrainView(generics.RetrieveAPIView):
    """API view for finding the next simultaneous train arrival time."""

    serializer_class = TrainScheduleSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve the next simultaneous train arrival time.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response object.

        Raises:
            ValueError: If the time parameter is missing or has an invalid format.
        """
        time = self.request.query_params.get("time")
        if not time:
            return Response({"error": "Missing time parameter"}, status=400)

        try:
            query_time = datetime.strptime(time, "%I:%M %p")
        except ValueError:
            return Response(
                {"error": "Invalid time format. Please use HH:MM AM/PM"}, status=400
            )

        station_schedule = get_station_schedule()

        simultaneous_time = find_next_simultaneous_time(station_schedule, query_time)

        if not simultaneous_time:
            simultaneous_time = find_next_day_simultaneous_time(station_schedule)

        if simultaneous_time:
            return Response(
                {"next_simultaneous_time": simultaneous_time.strftime("%I:%M %p")},
                status=200,
            )
        return Response(status=200)
