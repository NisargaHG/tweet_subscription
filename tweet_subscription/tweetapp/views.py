import razorpay
from django.utils.timezone import now
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from pytz import timezone
from .models import SubscriptionPlan, UserSubscription, Payment
from .forms import PaymentForm
from .utils import generate_invoice_pdf
from django.core.mail import EmailMessage
from .utils import generate_invoice_pdf
from django.core.mail import EmailMessage



client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

def is_payment_time():
    ist = timezone('Asia/Kolkata')
    current_hour = now().astimezone(ist).hour
    return current_hour == 10  # Only between 10 AM to 11 AM




from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from pytz import timezone
from datetime import datetime
import razorpay
from .utils import generate_invoice_pdf  

@login_required
def pay(request):
    # Restrict payment to between 10 AM and 11 AM IST
    india = timezone('Asia/Kolkata')
    now = datetime.now(india)
    if not (10<= now.hour < 11):
        return HttpResponse("❌ Payment is only allowed between 10 AM and 11 AM IST.")

    # Plan pricing (in paise)
    plan_amounts = {
        "free": 0,
        "bronze": 10000,
        "silver": 30000,
        "gold": 100000,
    }

    if request.method == "POST":
        plan = request.POST.get("plan")
        amount = plan_amounts.get(plan)

      
        

        # -*- coding: utf-8 -*-

        if plan == "free":
            

            pdf = generate_invoice_pdf(
                "Free",
                0,
                now.strftime('%d-%m-%Y %H:%M:%S')
            )

            subject = "✅ Free Plan Activated - TweetApp"
            body = f"""
        Hello {request.user.username},

        🎉 You’ve successfully activated the Free Plan on TweetApp!

        🧾 Invoice Summary:
        ----------------------------
        Plan Name: Free
        Amount Paid: Rs. 0.00
        Date: {now.strftime('%d-%m-%Y %H:%M:%S')}

        Enjoy tweeting!

        TweetApp Team 🐦
            """

            email = EmailMessage(subject, body, to=[request.user.email])
            email.attach(f"Invoice_Free.pdf", pdf.read(), 'application/pdf')
            email.send()
            messages.success(request, f"✅ Subscribed to  free plan! Invoice sent to {request.user.email}.")
            return render(request, "tweetapp/payment.html")

    
        
        # Razorpay Order
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
        payment = client.order.create({
            'amount': amount,
            'currency': 'INR',
            'payment_capture': '1'
        })
        

        # Generate Invoice PDF
        invoice_pdf = generate_invoice_pdf(
            plan_name=plan.capitalize(),
            amount=amount / 100,
            date=now.strftime('%d-%m-%Y %H:%M:%S')
        )

        # Send Email with invoice
        subject = f"✅ TweetApp - {plan.capitalize()} Plan Subscription Confirmation"
        body = f"""
Hello {request.user.username},

Thank you for subscribing to the {plan.capitalize()} Plan on TweetApp!

🧾 Invoice Summary:
---------------------------
Plan: {plan.capitalize()}
Amount: ₹{amount / 100:.2f}
Date: {now.strftime('%d-%m-%Y %H:%M:%S')}

Regards,
TweetApp Team
        """
        email = EmailMessage(subject, body, to=[request.user.email])
        email.attach(f"Invoice_{plan}.pdf", invoice_pdf.read(), 'application/pdf')
        email.send()

        # Success Message
        messages.success(request, f"✅ Subscribed to {plan.capitalize()} plan! Invoice sent to {request.user.email}.")
        return render(request, "tweetapp/payment.html", {"payment": payment})

    return render(request, "tweetapp/choose_plan.html")

