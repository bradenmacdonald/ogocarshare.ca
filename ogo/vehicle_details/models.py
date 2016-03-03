""" vehicle_details models """
from django.db import models
from filer.fields.image import FilerImageField


class VehicleDetails(models.Model):
    """ Optional image and description of each car in the fleet """
    engage_id = models.IntegerField(
        unique=True,
        verbose_name="Car #",
        help_text="The vehicle's ID/# as seen in Engage.",
    )
    name = models.CharField(
        blank=False,
        max_length=255,
        help_text="Name is not shown to visitors, since the name from Engage is used.",
    )
    description = models.TextField(blank=True)
    image = FilerImageField(blank=True)

    def has_image(self):
        return bool(self.image)
    has_image.boolean = True

    class Meta:
        verbose_name_plural = "Vehicle Details"
