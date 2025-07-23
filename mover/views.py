from django.contrib.auth.decorators import login_required
@login_required
def cancel_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id, customer=request.user)
    if booking.status == 'Pending':
        booking.status = 'Cancelled'
        booking.save()
    return redirect('dashboard')
def contact(request):
    if request.method == 'POST':
        # Here you could handle the contact form submission (e.g., send email)
        pass
    return render(request, 'mover/contact.html')
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, BookingForm, ReviewForm
from .models import Booking, Review
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    return render(request, 'mover/home.html')

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'mover/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'mover/login.html')

@login_required
def dashboard(request):
    bookings = Booking.objects.filter(customer=request.user)
    return render(request, 'mover/dashboard.html', {'bookings': bookings})

@login_required
def book_move(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.estimated_cost = 5000  # Replace with logic
            booking.save()
            # Send email notification
            subject = f"New Move Booking from {request.user.username}"
            try:
                phone = request.user.profile.phone
            except Exception:
                phone = 'N/A'
            message = (
                f"A new move has been booked!\n\n"
                f"Customer: {request.user.username}\n"
                f"Email: {request.user.email}\n"
                f"Phone: {phone}\n"
                f"Origin: {booking.origin}\n"
                f"Destination: {booking.destination}\n"
                f"Date: {booking.date}\n"
                f"Items: {booking.items_description}\n"
                f"Estimated Cost: {booking.estimated_cost}\n"
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [getattr(settings, 'BOOKING_NOTIFICATION_EMAIL', settings.DEFAULT_FROM_EMAIL)],
                fail_silently=True,
            )
            return redirect('dashboard')
    else:
        form = BookingForm()
    return render(request, 'mover/book_move.html', {'form': form})

@login_required
def booking_status(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'mover/booking_status.html', {'booking': booking})

@login_required
def submit_review(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.save()
            return redirect('dashboard')
    else:
        form = ReviewForm()
    return render(request, 'mover/review.html', {'form': form})

