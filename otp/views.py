from django.db import reset_queries
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import *
from otp.models import product
import random
import datetime
import socket
import re
import json
from urllib.request import urlopen
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#view for shop
#view for buy now
#view for bank details 
#view for otp 
#view for successfull transaction

def shop(request):
    products = product.objects.filter()
    return render(request,'shop.html',{
        'products': products,
    })

def buynow(request,pk):
    pro = product.objects.filter(id = pk)[0]
    return render(request,'buynow.html',{
        'product':pro,
    })

def bankdetails(request,pk):
    pro = product.objects.filter(id = pk)[0]
    return render(request,'bankdetails.html',{
        'product':pro,
    })
    

def generateotp():
    return random.randint(1000,9999)

def getip():
    hostname = socket.gethostname()
    print(hostname)     
    return socket.gethostbyname(hostname)

def getlocation():
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)

    IP=data['ip']
    org=data['org']
    city = data['city']
    country=data['country']
    region=data['region']

    return str(city)+','+str(region)+','+str(country)

def sendemail(email,otp,location,ip,amount):
    sender_email = 'smsedu.receive@gmail.com'
    message = MIMEMultipart()
    message['Subject'] = "OTP" 
    body = "Your OTP to complete transaction is: " + str(otp) +"\nAmount: "+ str(amount)+ "\nLocation: " + str(location) + "\n IP Adress: " + str(ip)
    message.attach(MIMEText(body, 'plain'))
    print(message)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender_email,'Sms@edu1234')
    s.sendmail(sender_email, email, message.as_string())
    s.quit()


def otp(request,pk):
    if request.method == 'POST':
        Cardnumber = request.POST.get('cardnumber')
        expiry = request.POST.get('exp')
        Cvv = request.POST.get('cvv')
        pro = product.objects.filter(id=pk)[0]
        expyear = int(expiry[0:4])
        expmonth = int(expiry[5:])
        print(expmonth,expyear)
        card = cards.objects.filter(cardnumber = Cardnumber,expYear = expyear, expMonth = expmonth, cvv = Cvv)
        if card :
            newotp = generateotp()
            location = getlocation()
            ip = getip()
            print(newotp,location,ip)
            sendemail(card[0].email,newotp,location,ip,pro.price)
            o = Otp(cardnumber = Cardnumber, code = newotp)
            o.save()
            #send otp
            if pro.price > card[0].highamount:
                return render(request,'enterotpbig.html',{
                    'product':pro,
                    'cardnumber':Cardnumber,
                    'expiry':expiry,
                    'cvv':Cvv,
                    'question':card[0].securityquestion,
                })
            else:
                return render(request,'enterotp.html',{
                    'product':pro,
                    'cardnumber':Cardnumber,
                    'expiry':expiry,
                    'cvv':Cvv,
                })
        else:
            return render(request,'wrongcarddetails.html',{

            })



def transactionsmall(request,pk):
    if request.method == 'POST':
        Cardnumber = request.POST.get('cardnumber')
        expiry = request.POST.get('exp')
        Cvv = request.POST.get('cvv')
        OTp = request.POST.get('otp')
        pro = product.objects.filter(id=pk)[0]
        expyear = int(expiry[0:4])
        expmonth = int(expiry[5:])
        card = cards.objects.filter(cardnumber = Cardnumber,expYear = expyear, expMonth = expmonth, cvv = Cvv)[0]
        otps = Otp.objects.filter(cardnumber = Cardnumber,code = OTp)
        if otps:
            d = otps[0].delete()
            tran = Trasaction(product = pro, ip = str(getip()),card = card)
            tran.save()
            return render(request,'success.html',{

            })
        else:
            return render(request,'wrongotp.html',{

            })
    pass

def transactionbig(request,pk):
    if request.method == 'POST':
        Cardnumber = request.POST.get('cardnumber')
        expiry = request.POST.get('exp')
        Cvv = request.POST.get('cvv')
        OTp = request.POST.get('otp')
        answer = request.POST.get('answer')
        pro = product.objects.filter(id=pk)[0]
        expyear = int(expiry[0:4])
        expmonth = int(expiry[5:])
        card = cards.objects.filter(cardnumber = Cardnumber,expYear = expyear, expMonth = expmonth, cvv = Cvv)[0]
        otps = Otp.objects.filter(cardnumber = Cardnumber,code = OTp)
        print(otps)
        if otps and answer == card.securityans:
            d = otps[0].delete()
            tran = Trasaction(product = pro, ip = str(getip()),card = card)
            tran.save()
            return render(request,'success.html',{

            })
        else:
            return render(request,'wrongotp.html',{

            })
    pass


