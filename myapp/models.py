# Create your models here.
from django.db import models


# Create your models here.

class Venue(models.Model):
    venue_name = models.CharField(max_length=30)
    form_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "List of Venue"

    def __str__(self):
        return self.venue_name


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    
    class Meta:
        verbose_name_plural = "List of Users"

    def __str__(self):
        return self.email
    



class Book(models.Model):
    BOOKED = 'B'
    CANCELLED = 'C'

    TICKET_STATUSES = ((BOOKED, 'Booked'),
                       (CANCELLED, 'Cancelled'),)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    staff_data = models.CharField(max_length=30, null=True, blank=True)
    userid =models.DecimalField(decimal_places=0, max_digits=2)
    venueid=models.ForeignKey(Venue, on_delete=models.CASCADE, null=True, blank=True)
    venue_name = models.CharField(max_length=30)
    
    
    form_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)

    status = models.CharField(choices=TICKET_STATUSES, default=BOOKED, max_length=2)

    class Meta:
        verbose_name_plural = "List of Books"
    def __str__(self):
        return self.email
    
