from django.core.validators import RegexValidator
from django.db import models


class TrainSchedule(models.Model):
    """
    Model representing a train schedule.

    Attributes:
        name (str): Name of the train line (1 to 4 alphanumeric characters).
        schedule (str): Schedule of train arrivals at the station.
    """

    name_validator = RegexValidator(
        regex=r"^[a-zA-Z0-9]{1,4}$",
        message="Name should contain 1 to 4 alphanumeric characters.",
    )

    name = models.CharField(
        max_length=4,
        validators=[name_validator],
        unique=True,
        help_text="Name of the train line (1 to 4 alphanumeric characters)",
    )
    schedule = models.TextField()

    def __str__(self):
        """
        Return a string representation of the TrainSchedule object.

        Returns:
            str: The name of the train line.
        """
        return self.name
