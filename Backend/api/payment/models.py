from django.db import models

class Payment(models.Model):
    user = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    total_amount = models.CharField(max_length=100)
    transaction_code= models.CharField(max_length=500)
    courseid = models.CharField(max_length=100)
    transaction_uuid = models.CharField(max_length=500)
    status = models.CharField(max_length=500)
    def __str__(self):
        return f"{self.user} - {self.email}"