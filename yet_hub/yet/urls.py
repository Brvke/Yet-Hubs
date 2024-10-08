from django.contrib.auth import views as auth_views
from django.urls import path
from .views import venue_list, venue_detail, create_booking, owner_dashboard


from . import views
from .forms import LoginForm

app_name = 'yet'

urlpatterns = [
    path('', views.index, name='index'),
    path('', venue_list, name='venue_list'),
    path('venue/<int:venue_id>/', venue_detail, name='venue_detail'),
    path('venue/<int:venue_id>/book/', create_booking, name='create_booking'),
    path('owner/dashboard/', owner_dashboard, name='owner_dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='yet/login.html', authentication_form=LoginForm), name='login'),
]