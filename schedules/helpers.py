from datetime import datetime
from typing import List, Union

from schedules.models import TrainSchedule


def get_station_schedule() -> List[str]:
    """
    Retrieve the station schedule.

    Returns:
        List[str]: The list of arrival times in the station schedule.
    """
    entire_schedule = TrainSchedule.objects.values_list("schedule", flat=True)
    station_schedule = [
        time.strip() for schedule in entire_schedule for time in schedule.split(",")
    ]
    return sorted(station_schedule)


def find_next_simultaneous_time(
    station_schedule: List[str], query_time: datetime
) -> Union[datetime, None]:
    """
    Find the next simultaneous arrival time of multiple trains.

    Args:
        station_schedule (List[str]): The station schedule.
        query_time (datetime): The specified query time.

    Returns:
        Union[datetime, None]: The next simultaneous arrival time, or None if not found.
    """
    for arrival_time in station_schedule:
        train_time = datetime.strptime(arrival_time.strip(), "%I:%M %p")
        if train_time > query_time and station_schedule.count(arrival_time) >= 2:
            return train_time

    return None


def find_next_day_simultaneous_time(
    station_schedule: List[str],
) -> Union[datetime, None]:
    """
    Find the next simultaneous arrival time of multiple trains on the next day.

    Args:
        station_schedule (List[str]): The station schedule.

    Returns:
        Union[datetime, None]: The next simultaneous arrival time on the next day,
        or None if not found.
    """
    simultaneous_time = find_next_simultaneous_time(
        station_schedule=station_schedule,
        query_time=datetime.strptime("12:00 AM", "%I:%M %p"),
    )

    return simultaneous_time if simultaneous_time else None
