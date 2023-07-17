from django.urls import path

from .views import NextSimultaneousTrainView, TrainScheduleListCreateView

urlpatterns = [
    path(
        "trains/",
        TrainScheduleListCreateView.as_view(),
        name="train-schedule-list-create",
    ),
    path(
        "trains/next_simultaneous/",
        NextSimultaneousTrainView.as_view(),
        name="next-simultaneous-train",
    ),
]
