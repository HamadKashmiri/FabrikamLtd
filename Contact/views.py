#Code by Finlay Campbell
from django.shortcuts import render
from django.shortcuts import redirect
from Contact.forms import suppTicketForm
from Contact.models import suppTicket
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings

def contact(request):
    form = suppTicketForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            email = request.POST.get('email')
            name = request.POST.get('name')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            email_from = settings.EMAIL_HOST_USER
            user_email = [email]
            recipient_list = [settings.EMAIL_HOST_USER]
            content = (message + " from " + name + " reply to " + email) 
            email = EmailMessage(subject,content,email_from,recipient_list)
            email.send()
            subject = ("Support Ticket")
            content = ("Your support ticket has been recieved, we will be in touch shortly!")
            email = EmailMessage(subject, content,email_from,user_email)
            email.send()

            return redirect("Contact")
    else:
        return render(request, 'Contact/contact.html', {'form': form})

