from django.urls import path
from . import views

# Import necessary modules and views

urlpatterns = [
    # Define URL patterns for the views
    path('retrieve_event_data/', views.retrieve_event_data, name='retrieve_event_data'),
    path('send_event_emails/', views.send_event_emails, name='send_event_emails'),
    path('templates/', views.templates, name='templates'),
]