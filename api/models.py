from django.db import models

# Create your models here.


class Expense(models.Model):
    created_by = models.CharField(max_length=255, editable=False)
    created_on = models.CharField(max_length=255, editable=False)
    purchase_date = models.DateField(blank=True)  #I was thinking we should add a date and time for tracking
    item = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    amount = models.IntegerField()

    class Meta:
        db_table = 'expense'