from django.db import models


class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=500, null=True)
    url = models.URLField(null=True)

    def __str__(self):
        return self.url[:20] + self.phone_number

class MacID(models.Model):
    mac_id = models.CharField(max_length=200)
    