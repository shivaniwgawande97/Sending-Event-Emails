from django.contrib import admin
from .models import EmailTemplate, Employee, Event, EmailLog

# Import necessary modules and models

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):    
    # Admin interface for the Event model                                 
    list_display = ('event_type', 'event_date', 'employee')
    

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # Admin interface for the Employee model
    list_display = ('name', 'email')
    
    
@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    # Admin interface for the EmailTemplate model
    list_display = ('event_type','template')
    

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    # Admin interface for the EmailLog model
    list_display = ('event','status', 'error')

