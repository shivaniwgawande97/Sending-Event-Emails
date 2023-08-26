from django.db import models

# Import necessary modules

class Employee(models.Model):
    # Model to represent an employee
    name = models.CharField(max_length=100)
    email = models.EmailField()
   
    def __str__(self):
        return self.name


class Event(models.Model):
    # Model to represent an event
    EVENT_TYPES = [
        ('birthday', 'Birthday'),
        ('work_anniversary', 'Work Anniversary'),
    ]                                                                            
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    event_date = models.DateField()

    def __str__(self):
        return f"{self.employee.name}'s {self.event_type} on {self.event_date}"


class EmailTemplate(models.Model):
    # Model to represent an email template
    event_type = models.CharField(max_length=20, choices=Event.EVENT_TYPES)
    template = models.CharField(max_length=100)

    def __str__(self):
        return self.template


class EmailLog(models.Model):
    # Model to represent a log of sent emails
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=[('sent', 'Sent'), ('failed', 'Failed')])
    error = models.TextField(null=True)

    def __str__(self):
        return f"Email {self.status} for {self.event}"

