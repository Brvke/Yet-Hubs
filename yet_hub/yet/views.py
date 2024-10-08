from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import AuthenticationForm
from .models import Venue, Booking
from django.contrib.auth import authenticate, login
from .forms import SignupForm, BookingForm
from django.shortcuts import render, redirect, get_object_or_404



# Create your views here.
def index(request):
    return render(request, 'yet/index.html')

def contact(request):
    return render(request, 'yet/contact.html')


@login_required
def venue_list(request):
    venues = Venue.objects.all()
    return render(request, 'venue_list.html', {'venues': venues})

def venue_detail(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    return render(request, 'rental/venue_detail.html', {'venue': venue})

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

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('venue_list')
    else:
        form = AuthenticationForm()
    return render(request, 'yet/login.html', {'form': form})

def create_booking(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.venue = venue
            booking.save()
            return redirect('venue_list')  # Redirect to a suitable page
    else:
        form = BookingForm()
    return render(request, 'yet/create_booking.html', {'form': form, 'venue': venue})

def owner_dashboard(request):
    user = request.user
    venues = Venue.objects.filter(owner=user)
    bookings = Booking.objects.filter(venue__owner=user)
    return render(request, 'yet/owner_dashboard.html', {
        'venues': venues,
        'bookings': bookings,
    })