from rest_framework import status
from rest_framework.test import APITestCase

from .models import TrainSchedule


class TrainScheduleTests(APITestCase):
    """
    Test cases for the TrainSchedule API.

    Attributes:
        schedule1 (TrainSchedule): A TrainSchedule object created for testing.
        schedule2 (TrainSchedule): Another TrainSchedule object created for testing.
    """

    def setUp(self):
        """
        Set up the test data before running each test case.
        """
        self.schedule1 = TrainSchedule.objects.create(
            name="AB12", schedule="10:00 AM, 11:30 AM, 2:15 PM, 4:45 PM"
        )
        self.schedule2 = TrainSchedule.objects.create(
            name="CD34", schedule="9:30 AM, 10:00 AM, 11:00 AM, 11:30 AM, 1:00 PM"
        )

    def test_create_train_schedule(self):
        """
        Test creating a new train schedule via the API.
        """
        url = "/api/trains/"
        data = {"name": "EF56", "schedule": "8:00 AM, 9:00 AM, 12:00 PM, 3:00 PM"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TrainSchedule.objects.count(), 3)

    def test_retrieve_next_simultaneous_train(self):
        """
        Test retrieving the next simultaneous train arrival time after a specified time.
        """
        url = "/api/trains/next_simultaneous/"
        query_time = "10:30 AM"
        response = self.client.get(f"{url}?time={query_time}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["next_simultaneous_time"], "11:30 AM")

    def test_retrieve_next_simultaneous_train_no_simultaneous_time(self):
        """
        Test retrieving the next simultaneous train arrival time after a specified
        time when there is no simultaneous time.
        """
        url = "/api/trains/next_simultaneous/"
        query_time = "4:00 PM"
        response = self.client.get(f"{url}?time={query_time}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["next_simultaneous_time"], "10:00 AM")

    def test_retrieve_next_simultaneous_train_next_day(self):
        """
        Test retrieving the next simultaneous train arrival time on the next day.
        """
        url = "/api/trains/next_simultaneous/"
        query_time = "11:45 PM"
        response = self.client.get(f"{url}?time={query_time}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["next_simultaneous_time"], "10:00 AM")
