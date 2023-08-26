from django.core.mail import send_mail
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Event, EmailTemplate, Employee, EmailLog

# Import necessary modules and models

@csrf_exempt
def retrieve_event_data(request):
    # View to retrieve event data from the database and return it as a JSON response
    try:
        events = Employee.objects.all() 
        event_data = [{'name': event.name, 'date': event.email} for event in events]
        return JsonResponse({'events': event_data, 'message': 'Event data retrieved successfully.'})
    except Exception as e:
        return JsonResponse({'error': str(e)})


@csrf_exempt
def send_event_emails(request):
    # View to send event reminder emails to employees.
    current_date = timezone.now().date()
    events_today = Event.objects.filter(event_date=current_date)

    if not events_today.exists():
        # If there are no events scheduled for today, log that no events are scheduled and return a JSON response.
        EmailLog.objects.create(event=None, status='no events')
        return JsonResponse({'message': 'No events scheduled for today'})

    for event in events_today:
        # For each event scheduled for today
        try:
            employee = Employee.objects.get(id=event.employee_id)
            email_templates = EmailTemplate.objects.filter(event_type=event.event_type)
            if email_templates:
                # If an email template is found for the event type, use it to send an email to the employee.
                email_template = email_templates.first()
                email_content = email_template.template.format(employee_name=employee.name, event_date=event.event_date)

            max_attempts = 3
            for attempt in range(max_attempts):
                # Retry sending the email up to max_attempts times before logging it as a failed attempt.

                try:
                    send_mail(
                        subject=f"Event Reminder: {event.event_type.capitalize()}",
                        message=email_content,
                        from_email='shivamdhande331@gmail.com',           
                        recipient_list=['your_email_id@gmail.com'],
                        fail_silently=False,
                    )

                    # Log successful email sending.
                    EmailLog.objects.create(event=event, status='sent')
                    break

                except Exception as e:
                    if attempt == max_attempts - 1:
                        # Log failed email sending after max_attempts.
                        EmailLog.objects.create(event=event, status='failed', error=str(e))
            else:
                pass
           
        except EmailTemplate.DoesNotExist:
            return HttpResponse("Template does not Exist.")
        
    return JsonResponse({'message': 'Event emails sent successfully.'})


def templates(request):
    # View to retrieve all email templates from the database and return them as a JSON response.
    templates = EmailTemplate.objects.all()
    data = [{'event_type': template.event_type, 'template': template.template} for template in templates]
    return JsonResponse(data, safe=False)