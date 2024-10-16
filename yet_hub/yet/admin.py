from django.contrib import admin
from .models import Venue, Review, Booking, Profile
# Register your models here.

admin.site.register(Profile)
"""class VenueImageInline(admin.TabularInline):
    model = VenueImage
    extra = 1  # Number of empty forms to display """

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1  # Number of empty forms to display

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'rental_price', 'created_at')
    search_fields = ('name', 'location')
    
    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="100" />'
        else:
            return 'No Image'
    image_tag.allow_tags = True
    image_tag.short_description = 'Image Preview'

"""@admin.register(VenueImage)
class VenueImageAdmin(admin.ModelAdmin):
    list_display = ('venue', 'image')
    search_fields = ('venue__name',)  # Search by venue name"""

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('venue', 'user', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('user__username', 'venue__name')

"""@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('user__username', 'message')"""

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('venue', 'user', 'booking_date', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'venue__name')