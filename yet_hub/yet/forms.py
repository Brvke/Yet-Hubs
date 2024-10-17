import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Booking, Venue, Review
from .models import Profile


# login form
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})


# signup form
#class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

class SignupForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=Profile.USER_TYPES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')

    # Customizing widgets (for appearance)
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

# booking form
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_date', 'event_type']

        widgets = {
            'booking_date': forms.DateInput(attrs={
                'type': 'date',
                'min': datetime.date.today().strftime('%Y-%m-%d')  # Disable past dates,
                
            }),
        }

    # def __init__(self, *args, **kwargs):
    #     self.venue = kwargs.pop('venue', None)  # Expect venue to be passed
    #     super().__init__(*args, **kwargs)
        
    #     if self.venue:
    #         booked_dates = Booking.objects.filter(venue=self.venue).values_list('booking_date', flat=True)
    #         # Pass booked dates as a comma-separated list to the template (for JavaScript)
    #         self.fields['booking_date'].widget.attrs.update({
    #             'booked-dates': ','.join([date.strftime('%Y-%m-%d') for date in booked_dates])
    #         })

    # def clean_booking_date(self):
    #     booking_date = self.cleaned_data.get('booking_date')
    #     today = datetime.date.today()

    #     # Check if the selected booking date is in the past
    #     if booking_date <= today:
    #         raise forms.ValidationError("Booking date must be from tomorrow onward.")

    #     # Check if the date is already booked for the given venue
    #     if Booking.objects.filter(venue=self.venue, booking_date=booking_date).exists():
    #         raise forms.ValidationError("This date is already booked. Please choose another date.")

    #     return booking_date

# venue form
class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'location', 'capacity', 'rental_price', 'description', 'event_type']

# review form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']