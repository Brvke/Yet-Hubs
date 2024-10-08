from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Venue(models.Model):
    EVENT_TYPES = [
        ('Wedding', 'Wedding'),
        ('Meeting', 'Meeting'),
        ('Birthday', 'Birthday Party'),
        ('Other', 'Other'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    capacity = models.IntegerField()
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)

    def __str__(self):
        return self.name
    

class Booking(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateField()
    status = models.CharField(max_length=20, default='Pending')
    event_type = models.CharField(max_length=20, choices=Venue.EVENT_TYPES)

    def __str__(self):
        return f"Booking for {self.venue.name} by {self.user.username} on {self.booking_date}"