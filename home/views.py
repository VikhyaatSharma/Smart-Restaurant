from ast import Not
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from home.models import Tokens
from home.models import Menu
from home.models import Current_Orders
from home.models import Completed_Orders
from django.contrib.auth import get_user_model
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from email import message
import random
from datetime import date as date_n
from localStoragePy import localStoragePy
import threading

def index(request):
    local = localStoragePy('restaurant')
    if(request.method=="POST"):
        if(request.POST.get('mode')=="status"):
            tokens=str(local.getItem('smarttoken')[local.getItem('smarttoken').index(':')+3:local.getItem('smarttoken').index(':')+7])
            tok = (Tokens.objects.get(token=tokens))
            tok.status='status'
            tok.save()
            order = request.POST.get('order')
            curr = Current_Orders(token=tokens, items=order, table=1)
            curr.save()
            return redirect('/status')

    else:
        if(local.getItem('smarttoken') == None):
            return redirect('/signin')
        else:
            status = list(Tokens.objects.values())
            for i in status:
                if(i['token']==local.getItem('smarttoken')[local.getItem('smarttoken').index(':')+3:local.getItem('smarttoken').index(':')+7]):
                    status=i['status']
            if(status=='status'):
                return redirect('/status')
            elif(status=='delivered'):
                return redirect('/await')
            elif(status=='payment'):
                return redirect('/payment')
            else:
                data=list(Menu.objects.values())
                categories=[]
                for i in data:
                    if(i['category'] not in categories):
                        categories.append(i['category'])
                category_wise={}
                sublist=[]
                for i in range(len(categories)):
                    for j in data:
                        if(j['category']==categories[i]):
                            sublist.append(j)
                    category_wise[categories[i]]=sublist
                    sublist=[]
                
                context= {
                'categories': categories,
                'wise':category_wise
                }
                return render(request, "index.html", context)

def status(request):
    local = localStoragePy('restaurant')
    tokens=str(local.getItem('smarttoken')[local.getItem('smarttoken').index(':')+3:local.getItem('smarttoken').index(':')+7])
    if(request.method=="POST"):
        if(request.POST.get('mode')=="delivered"):
            tokens=str(local.getItem('smarttoken')[local.getItem('smarttoken').index(':')+3:local.getItem('smarttoken').index(':')+7])
            tok = (Tokens.objects.get(token=tokens))
            tok.status='payment'
            tok.save()
            return redirect('/payment')
    orders = list(Current_Orders.objects.values())
    nowget=[]
    for i in orders:
        if(i['token']==tokens):
            nowget=i['items']
    items=nowget.split(',')
    final=[]
    for i in range(0,len(items),3):
        temp=[]
        temp.append(items[i])
        temp.append(items[i+1])
        temp.append(items[i+2])
        temp.append(int(items[i+1])*int(items[i+2]))
        final.append(temp)
    net=0
    cgst=0.09
    sgst=0.09
    for i in final:
        net=net+i[-1]
    gross = net+(net*cgst)+(net*sgst)
    context={
        'order':final,
        "net":net,
        "cgst":cgst,
        "sgst":sgst,
        'gross':gross
    }
    return render(request, 'status.html', context=context)

def awaitt(request):
    local = localStoragePy('restaurant')
    if(request.method=="POST"):
        if(request.POST.get('mode')=="payment"):
            tokens=str(local.getItem('smarttoken')[local.getItem('smarttoken').index(':')+3:local.getItem('smarttoken').index(':')+7])
            tok = (Tokens.objects.get(token=tokens))
            tok.status='payment'
            tok.save()
            return redirect('/payment')
    return render(request, 'await.html')
def payment(request):
    local = localStoragePy('restaurant')
    tokens=str(local.getItem('smarttoken')[local.getItem('smarttoken').index(':')+3:local.getItem('smarttoken').index(':')+7])
    if(request.method=="POST"):
        if(request.POST.get('mode')=="done"):
            tokens=str(local.getItem('smarttoken')[local.getItem('smarttoken').index(':')+3:local.getItem('smarttoken').index(':')+7])
            tok = (Tokens.objects.get(token=tokens))
            tok.status='off'
            tok.save()
            bill = request.POST.get('bill')
            paymode = request.POST.get('paymode')
            item = request.POST.get('items')
            obj = Completed_Orders(token=tokens, items=item, paymentmode=paymode, total_payment=bill, date=date_n.today())
            obj.save()
            obj1 = Current_Orders.objects.get(token=tokens)
            print(obj1)
            obj1.delete()
            return redirect('/signout')
    orders = list(Current_Orders.objects.values())
    nowget=[]
    for i in orders:
        if(i['token']==tokens):
            nowget=i['items']
    items=nowget.split(',')
    final=[]
    for i in range(0,len(items),3):
        temp=[]
        temp.append(items[i])
        temp.append(items[i+1])
        temp.append(items[i+2])
        temp.append(int(items[i+1])*int(items[i+2]))
        final.append(temp)
    net=0
    cgst=0.09
    sgst=0.09
    for i in final:
        net=net+i[-1]
    gross = net+(net*cgst)+(net*sgst)
    context={
        'items':nowget,
        'token':tokens,
        'order':final,
        "net":net,
        "cgst":cgst,
        "sgst":sgst,
        'gross':gross
    }
    return render(request, 'payment.html' , context)

def signin(request):
    if(request.method == "POST"):
        token = request.POST.get('token')
        table = request.POST.get('table')
        valids = list(Tokens.objects.values())
        found=0
        for i in valids:
            if(i['token']==token):
                found=i
        if(found!=0):
            if(found['status']=='new'):
                local = localStoragePy('restaurant')
                local.setItem('smarttoken', {'token':token,'table':table})
                stats=(Tokens.objects.get(token=token))
                stats.status='idle'
                stats.table=table
                stats.save()
                return redirect('/')
            elif(found['status']=='off'):
                messages.error(request, "Tag isn't activated")
            elif(str(localStoragePy('restaurant').getItem('smarttoken')[localStoragePy('restaurant').getItem('smarttoken').index(':')+3:localStoragePy('restaurant').getItem('smarttoken').index(':')+7]) == token):
                return redirect('/')
            else:
                messages.error(request, 'Tag in use')
        else:
            messages.error(request, 'Invalid Tag')
            return render(request, 'login.html')
    return render(request, 'login.html')

def signout(request):
    local = localStoragePy('restaurant')
    local.clear()
    logout(request)
    messages.success(request, "Thank You")
    return redirect('/signin')
def stattokenchange(request):
    if(request.method == "POST"):
        token = request.POST.get('token')
        status = request.POST.get('status')
        obj = Tokens.objects.get(token=token)
        obj.status = status
        messages.success(request, 'Tag Status Updated')
        obj.save()
    return render(request,"stattokenchange.html")