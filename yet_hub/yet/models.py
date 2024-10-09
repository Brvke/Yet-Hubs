from django.db import models
from django.contrib.auth.models import User


# venue model
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

# booking model 
class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    event_type = models.CharField(max_length=20)  # e.g., Wedding, Meeting, etc.

    def __str__(self):
        return f"Booking for {self.venue.name} by {self.user.username} on {self.booking_date}"
    

# image model
class VenueImage(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='venue_images/')

    def __str__(self):
        return f"Image for {self.venue.name}"

# review model
class Review(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()  # e.g., 1 to 5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.venue.name} by {self.user.username}"

# notification model
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"