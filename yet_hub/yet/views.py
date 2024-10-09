from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test 
from .models import Venue, Booking, Notification, Review
from django.contrib.auth import authenticate, login
from .forms import SignupForm, BookingForm, VenueForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import LoginForm, ReviewForm
from django.contrib.auth.models import User

def index(request):
    return render(request, 'yet/index.html')

@login_required
def create_venue(request):
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user
            venue.save() 
            return redirect('yet/owner_dashboard')
    else:
        form = VenueForm()
    
    return render(request, 'yet/create_venue.html', {'form': form})

@login_required
def venue_detail(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    return render(request, 'yet/venue_detail.html', {'venue': venue})

@login_required
def venue_list(request):
    venues = Venue.objects.all()  # Retrieve all venues
    return render(request, 'yet/venue_list.html', {'venues': venues})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'yet/signup.html', {
        'form': form
    })

def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully.')
                return redirect('owner_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'yet/login.html', {'form': form})

@login_required
def create_booking(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.venue = venue
            booking.save()
            return redirect('venue_list')
    else:
        form = BookingForm(initial={'venue': venue})
    
    return render(request, 'yet/create_booking.html', {'form': form, 'venue': venue})


def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'yet/notification_list.html', {'notifications': notifications})


def submit_review(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.venue = venue
            review.save()
            return redirect('yet/venue_detail', venue_id=venue.id)
    else:
        form = ReviewForm()
        
    return render(request, 'yet/submit_review.html', {'form': form, 'venue': venue})


# admin dashboard
@user_passes_test(lambda u: u.is_superuser)  # Restrict access to superusers
def admin_dashboard(request):
    total_venues = Venue.objects.count()
    total_bookings = Booking.objects.count()
    total_users = User.objects.count()
    total_reviews = Review.objects.count()
    total_notifications = Notification.objects.count()

    context = {
        'total_venues': total_venues,
        'total_bookings': total_bookings,
        'total_users': total_users,
        'total_reviews': total_reviews,
        'total_notifications': total_notifications,
    }

    return render(request, 'yet/admin/dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser)
def venue_list(request):
    venues = Venue.objects.all()
    return render(request, 'yet/admin/venue_list.html', {'venues': venues})

# owner dashboard

@login_required
def owner_dashboard(request):
    user = request.user
    venues = Venue.objects.filter(owner=user)
    bookings = Booking.objects.filter(venue__owner=user)

    # Optional: Calculate total bookings and total revenue
    total_bookings = bookings.count()
    total_revenue = sum(booking.venue.rental_price for booking in bookings)

    return render(request, 'yet/owner_dashboard.html', {
        'venues': venues,
        'bookings': bookings,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
    })