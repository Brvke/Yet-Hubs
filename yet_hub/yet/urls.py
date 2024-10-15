from django.contrib.auth import views as auth_views
from django.urls import path
from .views import venue_list, venue_detail, create_booking, owner_dashboard, create_review, create_venue, admin_dashboard
from . import views
from .forms import LoginForm
from django.contrib.auth.views import LogoutView

app_name = 'yet'

urlpatterns = [
    path('', views.index, name='index'),
    path('venue/add/', create_venue, name='create_venue'),
    path('venues/', venue_list, name='venue_list'),
    path('venue/<int:venue_id>/', venue_detail, name='venue_detail'),
    path('venue/<int:venue_id>/book/', create_booking, name='create_booking'),
    path('dashboard/', owner_dashboard, name='owner_dashboard'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    #path('notifications/', notification_list, name='notification_list'),
    path('signup/', views.signup, name='signup'),
    path('venue/<int:venue_id>/review/', create_review, name='create_review'),
    path('login/', auth_views.LoginView.as_view(template_name='yet/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]