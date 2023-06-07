from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('findvenue', views.findvenue, name="findvenue"),
    path('bookings', views.bookings, name="bookings"),
    path('cancellings', views.cancellings, name="cancellings"),
    path('seebookings', views.seebookings, name="seebookings"),
    path('seeICR', views.seeICR, name="seeICR"),
    path('findICR', views.findICR, name="findICR"),
    path('seeAuditorium', views.seeAuditorium, name="seeAuditorium"),
    path('findAuditorium', views.findAuditorium, name="findAuditorium"),
    path('seeAnisur', views.seeAnisur, name="seeAnisur"),
    path('seeBonomaya', views.seeBonomaya, name="seeBonomaya"),
    
    
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('success', views.success, name="success"),
    path('signout', views.signout, name="signout"),

]
