import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Booking, Venue, Review

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
class SignupForm(UserCreationForm):
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

# booking form
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['venue', 'booking_date', 'event_type']

        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        if booking_date < datetime.date.today():
            raise forms.ValidationError("Booking date cannot be in the past.")
        return booking_date

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