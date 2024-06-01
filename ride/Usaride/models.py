from django.db import models

class Trip(models.Model):
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    displacement = models.FloatField()
    distance = models.FloatField()
    bearing = models.FloatField()
    nyc_dist = models.FloatField()
    day = models.IntegerField()
    hour = models.IntegerField()

    def __str__(self):
        return f'Trip from ({self.pickup_latitude}, {self.pickup_longitude}) to ({self.dropoff_latitude}, {self.dropoff_longitude})'
