from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test 
from .models import Venue, Booking, Review, Profile
from django.contrib.auth import authenticate, login
from .forms import SignupForm, BookingForm, VenueForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import LoginForm, ReviewForm, CustomLoginForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.db.models import Q

"""
def index(request):
    return render(request, 'yet/index.html')

@login_required
def venue_detail(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    return render(request, 'yet/venue_detail.html', {'venue': venue})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect(reverse('login'))
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
                return redirect(reverse('base.html'))
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'yet/login.html', {'form': form})

# custom user log in

class CustomLoginView(LoginView):
    form_class = CustomLoginForm  # Use the custom form

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        profile = user.profile  # Assuming you have a Profile model
        if profile.user_type == 'Owner':
            return redirect('owner_dashboard')
        return redirect('login')  

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

@login_required
def create_review(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.venue = venue
            review.user = request.user
            review.save()
            return redirect('venue_detail', pk=venue_id)
    else:
        form = ReviewForm()
    return render(request, 'venue_detail.html', {'form': form, 'venue': venue})


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
    profile = request.user.profile
    
    if profile.user_type != 'Owner':
        return redirect('yet:login_')
    
    venues = Venue.objects.filter(owner=profile)
    bookings = Booking.objects.filter(venue__owner=profile)
    owner_dashboard = reverse('owner_dashboard')
    # Optional: Calculate total bookings
    total_bookings = bookings.count()
    return render(request, 'yet/owner_dashboard.html', {
        'venues': venues,
        'bookings': bookings,
        'total_bookings': total_bookings,
        'dashboard_url': owner_dashboard,
    })

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

"""
# search 

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q

from .models import Venue, Booking, Profile, Review
from .forms import SignupForm, BookingForm, VenueForm, LoginForm, ReviewForm, CustomLoginForm

# Homepage view
def index(request):
    # Fetch all venues
    return render(request, 'yet/index.html')

# Signup view for both users and owners
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from .forms import SignupForm
from .models import Profile

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            
            user_type = form.cleaned_data.get('user_type')
            
            Profile.objects.create(user=user, user_type=user_type)

            login(request, user)
            
            return redirect(reverse('login')) 
    else:
        form = SignupForm()

    return render(request, 'yet/signup.html', {'form': form})



# Login view

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
                
                profile = user.profile 
                if profile.user_type == 'Owner':
                    return redirect(reverse('/admin/'))
                else:
                    return redirect(reverse('yet:index')) 
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'yet/login.html', {'form': form})

# View to create a venue (for owners)


# Venue detail view (for users)
@login_required
def venue_detail(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    return render(request, 'yet/venue_detail.html', {'venue': venue})

# Create booking (for users)
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
            return redirect('venue_detail', venue_id=venue_id)
    else:
        form = BookingForm()

    return render(request, 'yet/create_booking.html', {'form': form, 'venue': venue})

# Search functionality for users
def search_venues(request):
    query = request.GET.get('q')
    venues = Venue.objects.all()

    if query:
        venues = venues.filter(
            Q(name__icontains=query) | 
            Q(location__icontains=query) | 
            Q(capacity__gte=query)
        )

    return render(request, 'yet/search_results.html', {'venues': venues})

# View for all venues   
def venue_list(request):
    venues = Venue.objects.all()
    return render(request, 'yet/venue_list.html', {'venues': venues})

def venue_detail(request, venue_id):
    venue = get_object_or_404(Venue, pk=venue_id)
    return render(request, 'yet/venue_detail.html', {'venue': venue})