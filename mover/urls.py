from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book/', views.book_move, name='book_move'),
    path('status/<int:booking_id>/', views.booking_status, name='booking_status'),
    path('review/<int:booking_id>/', views.submit_review, name='submit_review'),
    path('contact/', views.contact, name='contact'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('logout/', views.logout_view, name='logout'),
]
