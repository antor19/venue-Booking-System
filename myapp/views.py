from datetime import datetime
from django.contrib import messages
from django.shortcuts import render
from decimal import Decimal

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Venue, Book
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.db.models import Q

from datetime import date, datetime, timedelta

def get_first_date_of_current_month(year, month):
    """Return the first date of the month.

    Args:
        year (int): Year
        month (int): Month

    Returns:
        date (datetime): First date of the current month
    """
    first_date = datetime(year, month, 1)
    return first_date.strftime("%Y-%m-%d")


def get_last_date_of_month(year, month):
    """Return the last date of the month.

    Args:
        year (int): Year, i.e. 2022
        month (int): Month, i.e. 1 for January

    Returns:
        date (datetime): Last date of the current month
    """

    if month == 12:
        last_date = datetime(year, month, 31)
    else:
        last_date = datetime(year, month + 1, 1) + timedelta(days=-1)

    return last_date.strftime("%Y-%m-%d")


def home(request):
    context = {}
    id_r = request.user.id
    book_list = Book.objects.filter(userid=id_r)
    context['book_list'] = book_list
    
    if request.user.is_authenticated:
        return render(request, 'myapp/home.html', context)
    else:
        return render(request, 'myapp/signin.html')


@login_required(login_url='signin')
def findvenue(request):
    context = {}
    venue = Venue.objects.all()
    
    if request.method == 'POST':
        venue_id = request.POST.get('venueid')
        month = request.POST.get('month')
        current_time = datetime.now()
        print('current_time = ', current_time)
        print("Year :", current_time.year)

        print('month = ', month)
        first = get_first_date_of_current_month(current_time.year, int(month))
        last = get_last_date_of_month(current_time.year, int(month))
        print('first -= ', first)
        print('last -= ', last)

        venue_list = Book.objects.filter(venueid__id=venue_id, form_date__gte=first, to_date__lte=last)
        print('booking list    = ', venue_list)
        
        context['venue_list'] = venue_list
        month = int(month)
        month = date(current_time.year, (month), 1).strftime('%B')
        context['month'] = month
        context['venue_data'] = Venue.objects.get(id=venue_id)
        return render(request, 'myapp/list.html', context=context)
    
        
    else:
        context['venue_list'] = venue
        return render(request, 'myapp/findICR.html', context)
   


@login_required(login_url='signin')
def bookings(request):
    context = {}
    if request.method == 'POST':
        venue_id = request.POST.get('venue_id')
        form_date = request.POST.get('form_date')
        to_date = request.POST.get('to_date')
        if to_date == '':
            to_date = None
        staff_data = request.POST.get('staff_data')
        venue = Venue.objects.get(id=venue_id)
        print('venue = ', venue)
        if venue:
            venue_name = venue.venue_name
            username_r = request.user.username
            email_r = request.user.email
            userid_r = request.user.id
            if to_date == None:
                venue_list = Book.objects.filter(venueid__id=venue_id, form_date__gte=form_date)
            else:
                venue_list = Book.objects.filter(venueid__id=venue_id, form_date__gte=form_date, to_date__lte=to_date)
            print('booking list    = ', venue_list)

            if len(venue_list)  == 0:

                
                
                book = Book.objects.create(name=username_r, email=email_r, userid=userid_r, venue_name=venue_name,
                                        venueid= Venue.objects.get(id=venue_id), form_date=form_date, to_date=to_date, staff_data= staff_data,
                                        status='BOOKED')
                print('------------book id-----------', book.id)
                book.save()
                context['book'] = Book.objects.get(id=book.id)
                return render(request, 'myapp/bookings.html', context=context)
            else:
                context['data'] = request.POST
                context["error"] = "Sorry select date already booking"
                return render(request, 'myapp/list.html', context)
        else:
            context['data'] = request.POST
            # context["error"] = "Sorry select fewer number of seats"
            return render(request, 'myapp/list.html', context)

    else:
        return render(request, 'myapp/list.html')



@login_required(login_url='signin')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        try:
            Book.objects.filter(id=booking_id).update(status='CANCELLED')
            messages.success(request, "Booked venue has been cancelled successfully.")
            return redirect(seebookings)
        except Book.DoesNotExist:
            context["error"] = "Sorry You have not booked that venue"
            return render(request, 'myapp/error.html', context)
    else:
        return render(request, 'myapp/findvenue.html')
    


@login_required(login_url='signin')
def seebookings(request,new={}):
    context = {}
    id_r = request.user.id
    book_list = Book.objects.filter(userid=id_r)
    if book_list:
        return render(request, 'myapp/booklist.html', locals())
    else:
        context["error"] = "Sorry no venue booked"
        return render(request, 'myapp/findvenue.html', context)





@login_required(login_url='signin')
def seeICR(request):
    context = {}  
    venue = Venue.objects.all()
    context['venue_list'] = venue
    return render(request, 'myapp/findICR.html', context)  


@login_required(login_url='signin')
def findICR(request):
    context = {}
    if request.method == 'POST':
        venue_id = request.POST.get('venueid')
        month = request.POST.get('month')
        current_time = datetime.now()
        print('current_time = ', current_time)
        print("Year :", current_time.year)

        print('month = ', month)
        first = get_first_date_of_current_month(current_time.year, int(month))
        last = get_last_date_of_month(current_time.year, int(month))
        print('first -= ', first)
        print('last -= ', last)

        venue_list = Book.objects.filter(venueid__id=venue_id, form_date__gte=first, to_date__lte=last)
        print('booking list    = ', venue_list)
        
        context['venue_list'] = venue_list
        context['venue_data'] = Venue.objects.get(id=venue_id)
        return render(request, 'myapp/list.html', context=context)
        
    else:
        return render(request, 'myapp/findICR.html')



@login_required(login_url='signin')
def seeAuditorium(request):
    context = {}  
    venue = Venue.objects.all()
    context['venue_list'] = venue
    return render(request, 'myapp/findAuditorium.html', context)  


@login_required(login_url='signin')
def seeAnisur(request):
    context = {}  
    venue = Venue.objects.all()
    context['venue_list'] = venue
    return render(request, 'myapp/findAnisur.html', context)  


@login_required(login_url='signin')
def seeBonomaya(request):
    context = {}  
    venue = Venue.objects.all()
    context['venue_list'] = venue
    return render(request, 'myapp/findBonomaya.html', context)  



@login_required(login_url='signin')
def findAuditorium(request):
    context = {}
    if request.method == 'POST':
        venue_id = request.POST.get('venueid')
        month = request.POST.get('month')
        current_time = datetime.now()
        print('current_time = ', current_time)
        print("Year :", current_time.year)

        print('month = ', month)
        first = get_first_date_of_current_month(current_time.year, int(month))
        last = get_last_date_of_month(current_time.year, int(month))
        print('first -= ', first)
        print('last -= ', last)

        venue_list = Book.objects.filter(venueid__id=venue_id, form_date__gte=first, to_date__lte=last)
        print('booking list    = ', venue_list)
        
        context['venue_list'] = venue_list
        context['venue_data'] = Venue.objects.get(id=venue_id)
        return render(request, 'myapp/list.html', context=context)
        
    else:
        return render(request, 'myapp/findICR.html')

def signup(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        email_r = request.POST.get('email')
        email_extension = 'diu.edu.bd'
        email_split = email_r.split("@")[1]
        print("email_split = ", email_split)
        password_r = request.POST.get('password')
        if email_split == email_extension:
            user = User.objects.create_user(name_r, email_r, password_r, )
            if user:
                login(request, user)
                return render(request, 'myapp/thank.html')
            else:
                context["error"] = "Provide Your DIU Email"
                return render(request, 'myapp/signup.html', context)
        else:
            context["error"] = "Provide Your DIU Email"
            return render(request, 'myapp/signup.html', context)
    else:
        return render(request, 'myapp/signup.html', context)


def signin(request):
    context = {}
    email_extension = 'diu.edu.bd'
    if request.method == 'POST':
        name_r = request.POST.get('name')
        password_r = request.POST.get('password')
        user_email = User.objects.filter(email=name_r)
        email = name_r.split('@')[1]
        if email == email_extension:
            if len(user_email) !=0:
                name_r = user_email[0].username
                user = authenticate(request, username=name_r, password=password_r)
                print('user = ', user)
                if user:
                    login(request, user)
                    # username = request.session['username']
                    context["user"] = name_r
                    context["id"] = request.user.id
                    return render(request, 'myapp/success.html', context)
                # return HttpResponseRedirect('success')
            else:
                context["error"] = "Provide Your DIU Email"
                return render(request, 'myapp/signin.html', context)
        else:
            context["error"] = "Provide Your DIU Email"
            return render(request, 'myapp/signin.html', context)
    else:
        context["error"] = "You are not logged in"
        return render(request, 'myapp/signin.html', context)


def signout(request):
    context = {}
    logout(request)
    context['error'] = "You have been logged out"
    return render(request, 'myapp/signin.html', context)


def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'myapp/success.html', context)
