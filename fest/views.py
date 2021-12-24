from django.shortcuts import render
from django.utils.regex_helper import flatten_result
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
import pyrebase
from qrcode import *
from fest.forms import *
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives 

import os


 
config={
    "apiKey": "AIzaSyB-ANIoewtFQ4wB7ylN7al5rovqy3Gf2KU",
  "authDomain": "braided-hangout-318911.firebaseapp.com",
  "databaseURL": "https://braided-hangout-318911-default-rtdb.firebaseio.com/",
  "projectId": "braided-hangout-318911",
  "storageBucket": "braided-hangout-318911.appspot.com",
  "messagingSenderId": "885844267940",
  "appId": "1:885844267940:web:5c7003a83607297e53a731",
  "measurementId": "G-4PBL2X0YFY"
}
firebase1=pyrebase.initialize_app(config)
authe = firebase1.auth()
database=firebase1.database()

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
context = {}
def index(request):
    
 
    return render(request, 'index.html')

@csrf_exempt
def paymenthandler(request):
 
  
    if request.method == "POST":
        try:
           
           
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            record=razorpay_client.payment.fetch(payment_id)
            data={"email":record["email"],"PhoneNumber":record["contact"]}
            strw=str(payment_id)
            
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                amount = context['razorpay_amount'] 
                try:
 
                    razorpay_client.payment.capture(payment_id, amount)
                    data["Name"]=str(context["form"].cleaned_data["Name"])
                    data["Club"]=str(context["form"].cleaned_data["Club"])
                    data["Event"]=str(context["form"].cleaned_data["Event"])
                    data["Fee"]=str(context["form"].cleaned_data["Fee"])
                    database.child(payment_id).set(data)
                    
                    
                    
                    img = make(strw)
                    img.save("fest/qrcode.png")
                    
                    subject = 'Django sending email'
                    body_html = '<html><body><H1>Hi</H1><img src="cid:qrcode.png"></body></html>'
                    from_email = settings.EMAIL_HOST_USER
                    to_email = data["email"]
                    fp = open(os.path.join(os.path.dirname(__file__), "qrcode.png"), 'rb')
                    msg_img = MIMEImage(fp.read())
                    fp.close()
                    msg_img.add_header('Content-ID', '<{}>'.format("qrcode.png"))
                    msg = EmailMultiAlternatives(
                        subject,
                        body_html,
                        from_email=from_email,
                        to=[to_email]
                    )
                    msg.mixed_subtype = 'related'
                    msg.attach_alternative(body_html, "text/html")
                    msg.attach(msg_img)
                    msg.send()
                    context["flag"]=False
                    context["form"]=None
                    return render(request, 'paymentsucess.html')
                except:
 
                    
                    return render(request, 'paymentfail.html',{"fail":"fail"})
            else:
 
               
                return render(request, 'paymentfail.html',{"fail":"sfail"})
        except:
 
           
            return HttpResponseBadRequest()
    else:
       
        return HttpResponseBadRequest()
    
def payform(request,event,fee):
    form=PayPage(initial={'Event':event,'Fee':int(fee)})
    currency = 'INR'
    
    razorpay_order = razorpay_client.order.create(dict(amount=int(fee)*100,currency=currency,payment_capture='0'))
 

    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'
 
    
    
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = int(fee)*100
    context['currency'] = currency
    context['callback_url'] = callback_url
    print(context['razorpay_amount'])
    if request.method == "POST":
        form=PayPage(request.POST or None)
        
        if form.is_valid():
            context["flag"]=True
            
    context["form"]=form
    return render(request,"hi.html",context)