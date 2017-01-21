"""
Models to store OGO gift certificate data
"""
from django.db import models


class GiftCert(models.Model):
    """ Represents a gift certificate bought as a gift for a member """
    recipient_name = models.CharField(
        max_length=256,
        blank=False,
        help_text=(
            "Enter the full name of the person whose account you would like us to credit. "
            "They must be an OGO member in good standing."
        ),
    )
    from_name = models.CharField(max_length=256, blank=False, verbose_name="From")
    from_email = models.EmailField(max_length=256, blank=False)
    from_phone = models.CharField(max_length=32, blank=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False)
    order_date = models.DateTimeField(auto_now_add=True, null=False)
    notes = models.TextField(blank=True)
    staff_notes = models.TextField(blank=True)
    paid = models.BooleanField(null=False, default=False)
    applied_to_account = models.BooleanField(null=False, default=False)
    confirmation_sent = models.BooleanField(null=False, default=False)

    def clean(self):
        for field in ("recipient_name", "from_name", "from_phone", "notes"):
            setattr(self, field, getattr(self, field).strip())

    class Meta:
        ordering = ("-order_date",)

    def __unicode__(self):
        return u"${} Gift to {} from {}".format(self.amount, self.recipient_name, self.from_name)
