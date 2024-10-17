from django.contrib.auth import views as auth_views
from django.urls import path
from .views import venue_detail, create_booking, venue_list
from . import views
from .forms import LoginForm
from django.conf import settings
from django.conf.urls.static import static

app_name = 'yet'

urlpatterns = [
    path('', views.index, name='index'),
    #path('venue/add/', create_venue, name='create_venue'),
    path('venue_list/', views.venue_list, name='venue_list'),
    path('venue/<int:venue_id>/', venue_detail, name='venue_detail'),
    path('venue/<int:venue_id>/book/', create_booking, name='create_booking'),
    #path('dashboard/', owner_dashboard, name='owner_dashboard'),
    #path('owner/dashboard/', owner_dashboard, name='owner_dashboard'),
    #path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    #path('notifications/', notification_list, name='notification_list'),
    path('signup/', views.signup, name='signup'),
    #path('venue/<int:venue_id>/review/', create_review, name='create_review'),
    path('login/', auth_views.LoginView.as_view(template_name='yet/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('login_/', CustomLoginView.as_view(), name='login_'),
    path('search/', views.search_result, name='search_result'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)