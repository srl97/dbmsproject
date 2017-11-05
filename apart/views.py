# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,render_to_response
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.db import connection
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
import datetime
from django.template.loader import get_template
from django.template import Context, Template,RequestContext
import hashlib
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf

# Create your views here.



def home(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM flatowner where username=%s",[request.user])
        rowv=cursor.fetchone()
    return(render(request, "home.html",{'rowv':rowv}))

def loginuser(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username=username, password=password)
        print user
        if user is not None:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM flatowner where username=%s",[user.username])
                row=cursor.fetchone()
            if row is not None:
                login(request,user)
                return(render(request,'userhome.html',{user:'user'}))
            return(render(request,'home.html',{'invalid':'invalid'}))
        return(render(request,'home.html',{'invalid':'invalid'}))

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM flatowner where username=%s",[request.user])
        rowv=cursor.fetchone()

    return(render(request,'home.html',{'rowv':rowv}))





def logoutuser(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM flatowner where username=%s",[request.user])
        rowv=cursor.fetchone()
    logout(request)
    return(render(request,'home.html',{'rowv':rowv}))
def adminlogout(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM admin where username=%s",[request.user])
        rowv=cursor.fetchone()

    logout(request)
    return(render(request,'admin.html',{'rowv':rowv}))

def adprofileview(request):
    user=request.user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM admin where username=%s",[request.user])
        rowv=cursor.fetchone()
    if request.method == 'POST':
        username=request.POST['username']
        if username=="":
            return(render(request,'adprofileview.html',{user:'user','data':data,'Invaliderr':'Error','rowv':rowv}))
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM parking where parking_user=%s",[username])
            rows=cursor.fetchall()
        with connection.cursor() as cursor:
            try:
                cursor.execute("SELECT * FROM flatowner WHERE username=%s",[username])
                data=cursor.fetchone()
                if data is not None:
                    return(render(request,'adprofileview.html',{user:'user','data':data,'rows':rows,'found':'found','rowv':rowv}))
                return(render(request,'adprofileview.html',{user:'user','Invaliderror':'No display','rowv':rowv}))


            except:
                return(render(request,'adprofileview.html',{user:'user','Invaliderror':'No display','rowv':rowv}))
    return(render(request,'adprofileview.html',{user:'user','rowv':rowv}))
def deletenotification(request):
    user=request.user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM admin where username=%s",[request.user])
        rowv=cursor.fetchone()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM notification")
        data=cursor.fetchall()


    if request.method == 'POST':
        notification_no=request.POST['notification_no']

        if notification_no=="":
            return(render(request,'del_notification.html',{user:'user','data':data,'Invaliderr':'Error','rowv':rowv}))
        with connection.cursor() as cursor:
            try:
                cursor.execute("DELETE FROM notification where notification_no='%s'"%(notification_no))
                return(render(request,'del_notification.html',{user:'user','data':data,'success':'success','rowv':rowv}))
            except:
                return(render(request,'del_notification.html',{user:'user','data':data,'Invaliderror':'No display','rowv':rowv}))
    return(render(request,'del_notification.html',{user:'user','data':data,'rowv':rowv}))

def delevents(request):
    user=request.user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM admin where username=%s",[request.user])
        rowv=cursor.fetchone()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM event")
        data=cursor.fetchall()


    if request.method == 'POST':
        event_name=request.POST['event_name']

        if event_name=="":
            return(render(request,'del_events.html',{user:'user','data':data,'Invaliderr':'Error','rowv':rowv}))
        with connection.cursor() as cursor:
            try:
                cursor.execute("DELETE FROM event where event_name='%s'"%(event_name))
                return(render(request,'del_events.html',{user:'user','data':data,'success':'success','rowv':rowv}))
            except:
                return(render(request,'del_events.html',{user:'user','data':data,'Invaliderror':'No display','rowv':rowv}))
    return(render(request,'del_events.html',{user:'user','data':data,'rowv':rowv}))

def adviewcomplain(request):
    user=request.user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM admin where username=%s",[request.user])
        rowv=cursor.fetchone()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM complaint")
        data=cursor.fetchall()


    if request.method == 'POST':
        complaint_id=request.POST['complaint_id']
        status=request.POST['status']
        print complaint_id,status
        if complaint_id=="" or status=="":
            return(render(request,'adviewcomplaints.html',{user:'user','data':data,'Invaliderr':'Error','rowv':rowv}))
        with connection.cursor() as cursor:
            try:
                cursor.execute("UPDATE complaint SET status='%s' where complaint_no='%s'"%(status,complaint_id))
                return(render(request,'adviewcomplaints.html',{user:'user','data':data,'success':'success','rowv':rowv}))
            except:
                return(render(request,'adviewcomplaints.html',{user:'user','data':data,'Invaliderror':'No display','rowv':rowv}))
    return(render(request,'adviewcomplaints.html',{user:'user','data':data,'rowv':rowv}))

def adnotification(request):
    user=request.user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM admin where username=%s",[request.user])
        rowv=cursor.fetchone()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM department")
        data=cursor.fetchall()
    if request.method == 'POST':
        not_no=request.POST['not_no']
        date=request.POST['date']
        title=request.POST['title']
        details=request.POST['details']
        issuer=request.POST['issuer']
        if not_no=="" or date=="" or title=="" or details==""or issuer=="":
            return(render(request,'adnotification.html',{user:'user','Invaliderror':'Missing','rowv':rowv}))
        with connection.cursor() as cursor:
                    try:
                        cursor.execute("INSERT INTO notification VALUES('%s','%s','%s','%s','%s')" %(not_no,date,details,issuer,title))


                        return(render(request,'adnotification.html',{user:'user','saved':'saved','data':data,'rowv':rowv}))

                    except:

                        return(render(request,'adnotification.html',{user:'user','Invalidrror':'Not saved','data':data,'rowv':rowv}))




    return(render(request,'adnotification.html',{user:'user','data':data,'rowv':rowv}))

def club_events(request):
    user=request.user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM admin where username=%s",[request.user])
        rowv=cursor.fetchone()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM club")
        data=cursor.fetchall()
    if request.method == 'POST':
        event_name=request.POST['event_name']
        event_date=request.POST['event_date']
        event_time=request.POST['event_time']
        event_venue=request.POST['event_venue']
        event_des=request.POST['event_des']
        organising_team=request.POST['organising_team']
        if event_name=="" or event_date=="" or event_time=="" or event_venue==""or organising_team=="":
            return(render(request,'club_events.html',{user:'user','Invaliderror':'Missing','rowv':rowv}))
        with connection.cursor() as cursor:
                    try:
                        cursor.execute("INSERT INTO event VALUES('%s','%s','%s','%s','%s','%s')" %(event_name,event_date,event_time,event_venue,event_des,organising_team))


                        return(render(request,'club_events.html',{user:'user','saved':'saved','data':data,'rowv':rowv}))

                    except:

                        return(render(request,'club_events.html',{user:'user','Invalidrror':'Not saved','data':data,'rowv':rowv}))
    return(render(request,'club_events.html',{user:'user','data':data,'rowv':rowv}))

def clubcancel(request):
    user=request.user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM admin where username=%s",[request.user])
        rowv=cursor.fetchone()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM membership where leaving_date is not NULL")
        data=cursor.fetchall()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM membership where leaving_date is NULL")
        datayes=cursor.fetchall()
    if request.method=='POST':
        username=request.POST['username']
        club_name=request.POST['club_name']
        if username=="" or club_name=="":
            return(render(request,'clubcancel.html',{user:'user','data':data,'datayes':datayes,'rowv':rowv,'empty':'empty'}))
        with connection.cursor() as cursor:
            try:
                cursor.execute("DELETE FROM membership where username='%s' and club_name='%s'"%(username,club_name))
                return(render(request,'clubcancel.html',{user:'user','data':data,'datayes':datayes,'success':'success','rowv':rowv}))
            except:
                return(render(request,'clubcancel.html',{user:'user','data':data,'datayes':datayes,'Error':'No display','rowv':rowv}))
    return(render(request,'clubcancel.html',{user:'user','data':data,'datayes':datayes,'rowv':rowv}))




















def depmanager(request):
    user=request.user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM admin where username=%s",[request.user])
        rowv=cursor.fetchone()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM department")
        data=cursor.fetchall()
    if request.method == 'POST':
            department=request.POST['department']
            dep_manager=request.POST['dep_manager']
            dep_phone=request.POST['dep_phone']
            dep_email=request.POST['dep_email']
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM flatowner where username=%s",[dep_manager])
                row=cursor.fetchone()
            if department=="" or dep_manager=="" or dep_phone=="" or dep_email=="" or row is None:
                return(render(request,'depmanager.html',{user:'user','data':data,'Invaliderr':'Error','rowv':rowv}))
            with connection.cursor() as cursor:
                try:
                    cursor.execute("UPDATE department SET dep_manager=%s,dep_phone=%s,dep_email=%s where dep_name=%s",(dep_manager,dep_phone,dep_email,department))
                    return(render(request,'depmanager.html',{user:'user','data':data,'saved':'success','rowv':rowv}))
                except:
                    return(render(request,'depmanager.html',{user:'user','data':data,'Invaliderror':'No display','rowv':rowv}))
    return(render(request,'depmanager.html',{user:'user','data':data,'rowv':rowv}))




def adminlog(request):


    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username=username, password=password)


        if user is not None:
            with connection.cursor() as cursor:
                cursor.execute("SELECT username FROM admin where username=%s",[user.username])
                row=cursor.fetchone()
                if row is not None:
                    login(request,user)
                    return(render(request,'admin.html',{user:'user','row':row}))
                return(render(request,'admin.html',{'invalid':'Error'}))
        return(render(request,'admin.html',{'invalid':'Error'}))


    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM admin where username=%s",[request.user])
        row=cursor.fetchone()

    return(render(request,'admin.html',{'row':row}))


def adduser(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM admin where username=%s",[request.user])
        rowv=cursor.fetchone()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO flatowner(username) values(%s)",[username])
            return render(request, 'adduser.html', {'form': form,'success':'success','rowv':rowv})
    else:
        form = UserCreationForm()
    return render(request, 'adduser.html', {'form': form,'rowv':rowv})

def profileview(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM flatowner where username=%s",[request.user])
        rowv=cursor.fetchone()
    user=request.user
    print user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM parking where parking_user=%s",[user])
        rows=cursor.fetchall()
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT * FROM flatowner WHERE username=%s",[user])
            data=cursor.fetchone()
            return(render(request,'profileview.html',{user:'user','data':data,'rows':rows,'rowv':rowv}))
        except:
            return(render(request,'profileview.html',{user:'user','Invaliderror':'No display','rowv':rowv}))
    return(render(request,'profileview.html',{user:'user','rowv':rowv}))

def adchange_password(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM admin where username=%s",[request.user])
        rowv=cursor.fetchone()
    user=request.user
    print user

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return(render(request,'adchangepassword.html',{user:'user','rowv':rowv,'success':'success'}))
        else:
            return(render(request,'adchangepassword.html',{user:'user','rowv':rowv,'nosuccess':'nosuccess'}))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'adchangepassword.html', {
        'form': form,'rowv':rowv
    })

def change_password(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM flatowner where username=%s",[request.user])
        rowv=cursor.fetchone()
    user=request.user

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return(render(request,'change_password.html',{user:'user','rowv':rowv,'success':'success'}))
        else:
            return(render(request,'change_password.html',{user:'user','rowv':rowv,'nosuccess':'nosuccess'}))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form,'rowv':rowv
    })

def addmaintenance(request):
    user=request.user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM admin where username=%s",[request.user])
        rowv=cursor.fetchone()
    if request.method == 'POST':
        bill_number=request.POST['billnumber']
        username=request.POST['username']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM flatowner where username=%s",[username])
            row=cursor.fetchone()
        print row
        if row is None:
            return(render(request,'addmaintenance.html',{'Invaliduser':'No display','rowv':rowv}))





        month=request.POST['month']
        cleaning_charge=request.POST['cleaning_charge']
        water_supply=request.POST['water_supply']
        electricity=request.POST['electricity']
        club_charges=request.POST['club_charges']
        security=request.POST['security']
        penalty=request.POST['penalty']
        status=request.POST['status']

        if bill_number=="" or username=="" or month=="" or cleaning_charge==""or water_supply==""or electricity==""or club_charges==""or security=="" or status=="":
            return(render(request,'addmaintenance.html',{user:'user','Invaliderror':'Missing','rowv':rowv}))
        total_sum=str(float(cleaning_charge)+float(water_supply)+float(electricity)+float(club_charges)+float(security)+float(penalty))
        with connection.cursor() as cursor:
                    try:
                        cursor.execute("INSERT INTO maintenance(bill_number,payeeuser,month,cleaning_charge,water_supply,electricity,club_charges,security,penalty,total_amount,status) VALUES('%s','%s','%s','%s''%s','%s','%s','%s','%s','%s')" %(bill_number,username,month,cleaning_charge,water_supply,electricity,club_charges,security,penalty,total_amount,status))


                        return(render(request,'addmaintenance.html',{user:'user','saved':'saved','rowv':rowv}))

                    except:

                        return(render(request,'addmaintenance.html',{user:'user','Invalidrror':'Not saved','rowv':rowv}))




    return(render(request,'addmaintenance.html',{user:'user','rowv':rowv}))


def clubs(request):
    user=request.user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM flatowner where username=%s",[request.user])
        rowv=cursor.fetchone()
    with connection.cursor() as cursor:
        cursor.execute("select e.* from event as e,membership as m where username=%s and m.leaving_date is NULL and e.organising_team=m.club_name",[request.user])
        rowevent=cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute("select c.* from club as c where c.club_name in(SELECT m.club_name FROM membership as m WHERE username=%s and leaving_date is NULL)",[user])
        datayes=cursor.fetchall()
    with connection.cursor() as cursor:
        cursor.execute("select club_name,leaving_date from membership where username=%s and leaving_date is not NULL",[user])
        datacancel=cursor.fetchall()
    with connection.cursor() as cursor:
        cursor.execute("select c.* from club as c where c.club_name not in(SELECT m.club_name FROM membership as m WHERE username=%s)",[user])
        datano=cursor.fetchall()

    print datayes



    if request.method == 'POST':
        club_name=request.POST.get('club')
        club_del=request.POST.get('clubdel')

        print club_name,club_del
        if club_del is None:
            joining_date=str(datetime.date.today())
            print joining_date
            with connection.cursor() as cursor:
                try:
                    cursor.execute("INSERT INTO membership(username,club_name,joining_date) values('%s','%s','%s')"%(user,club_name,joining_date))
                    return(render(request,'clubs.html',{user:'user','rowv':rowv,'success':'success'}))
                except:
                    return(render(request,'clubs.html',{user:'user','rowv':rowv,'failure':'failure'}))
        elif club_name is None:
            leaving_date=str(datetime.date.today())
            with connection.cursor() as cursor:
                try:
                    cursor.execute("UPDATE membership SET leaving_date=%s where username=%s and club_name=%s",(leaving_date,user,club_del))
                    return(render(request,'clubs.html',{user:'user','rowv':rowv,'successdel':'success'}))

                except:
                    return(render(request,'clubs.html',{user:'user','rowv':rowv,'failuredel':'failure'}))






    return(render(request,'clubs.html',{user:'user','datacancel':datacancel,'datayes':datayes,'rowevent':rowevent,'datano':datano,'rowv':rowv}))
def tenantview(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM admin where username=%s",[request.user])
        rowv=cursor.fetchone()
    user=request.user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tenant")
        rows=cursor.fetchall()
    return(render(request,'adviewtenant.html',{user:'user','rows':rows,'rowv':rowv}))
def deltenant(request):
    user=request.user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM flatowner where username=%s",[request.user])
        rowv=cursor.fetchone()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tenant where landlord_id=%s",[user])
        rows=cursor.fetchone()
    if request.method == 'POST':
        delete_on=request.POST['onvalue']
        if delete_on:
            with connection.cursor() as cursor:
                try:
                    cursor.execute("DELETE FROM tenant where landlord_id=%s",[user])
                    return(render(request,'deltenant.html',{user:'user','rows':rows,'rowv':rowv,'success':'success'}))
                except:
                    return(render(request,'deltenant.html',{user:'user','Invaliderror':'No display','rowv':rowv,'failure':'failure'}))




    return(render(request,'deltenant.html',{user:'user','rows':rows,'rowv':rowv}))


def tenant(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM flatowner where username=%s",[request.user])
        rowv=cursor.fetchone()
    user=request.user
    f=0
    l=0
    m=0
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tenant where landlord_id=%s",[user])
        rows=cursor.fetchone()
    if request.method == 'POST':
        name=request.POST['name']
        age=request.POST['age']
        if age.isdigit() is False:
            f=1
        else:
            if int(str(age))<18 or int(str(age))>120:
                f=1


        occupation=request.POST['occupation']
        phone=request.POST['phone']
        if phone.isdigit() is False or len(phone)!=10:
            l=1
        email=request.POST['email']

        if name=="" or age=="" or occupation=="" or phone=="":
            return(render(request,'tenant.html',{user:'user','Invalidrror':'Not saved','data':data,'rowv':rowv}))

        if f is 1 and l is 1:
            return(render(request,'tenant.html',{user:'user','invalidage':'Error','invalidphone':'Errorv','rowv':rowv}))
        if f is 0 and l is 1:
            return(render(request,'tennat.html',{user:'user','invalidphone':'Errorv','rowv':rowv}))
        if f is 1 and l is 0:
            return(render(request,'tenant.html',{user:'user','invalidage':'Errorv','rowv':rowv}))
        if rows is not None:


            with connection.cursor() as cursor:
                try:
                    cursor.execute("UPDATE tenant set name=%s,age=%s,occupation=%s,phone=%s,email=%s WHERE landlord_id=%s", (name,age,occupation,phone,email,user))
                    return(render(request,'tenant.html',{user:'user','rows':rows,'rowv':rowv,'success':'success'}))
                except:
                    return(render(request,'tenant.html',{user:'user','Invaliderror':'No display','rowv':rowv,'failure':'failure'}))
        if rows is None:


            with connection.cursor() as cursor:
                try:
                    cursor.execute("INSERT INTO tenant(name,age,occupation,phone,email,landlord_id) VALUES('%s','%s','%s','%s','%s','%s')" %(name,age,occupation,phone,email,user))
                    return(render(request,'tenant.html',{user:'user','rows':rows,'rowv':rowv,'success':'success'}))
                except:
                    return(render(request,'tenant.html',{user:'user','Invaliderror':'No display','rowv':rowv,'failure':'failure'}))




    return(render(request,'tenant.html',{user:'user','rows':rows,'rowv':rowv}))


def profileupdate(request):
    user=request.user
    f=0
    l=0
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM flatowner where username=%s",[request.user])
        rowv=cursor.fetchone()

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM flatowner WHERE username=%s",[user])
        data=cursor.fetchone()
    if request.method == 'POST':
        name=request.POST['name']
        age=request.POST['age']
        if age.isdigit() is False:
            f=1
        else:
            if int(str(age))<18 or int(str(age))>120:
                f=1


        occupation=request.POST['occupation']
        phone=request.POST['phone']
        if phone.isdigit() is False or len(phone)!=10:
            l=1
        email=request.POST['email']
        print name
        if name=="" or age=="" or occupation=="" or phone=="":
            return(render(request,'profile.html',{user:'user','Invalidrror':'Not saved','data':data,'rowv':rowv}))

        if f is 1 and l is 1:
            return(render(request,'profile.html',{user:'user','invalidage':'Error','invalidphone':'Errorv','rowv':rowv}))
        if f is 0 and l is 1:
            return(render(request,'profile.html',{user:'user','invalidphone':'Errorv','rowv':rowv}))
        if f is 1 and l is 0:
            return(render(request,'profile.html',{user:'user','invalidage':'Errorv','rowv':rowv}))





        with connection.cursor() as cursor:
            try:
                cursor.execute("UPDATE flatowner set name=%s,age=%s,occupation=%s,phone=%s,email=%s WHERE username=%s", (name,age,occupation,phone,email,user))


                return(render(request,'saved.html',{user:'user','saved':'saved','data':data,'rowv':rowv}))

            except:

                return(render(request,'profile.html',{user:'user','Invalidrror':'Not saved','data':data,'rowv':rowv}))


    return(render(request,'profile.html',{user:'user','data':data,'rowv':rowv}))

def notifications(request):
    user=request.user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM flatowner where username=%s",[request.user])
        rowv=cursor.fetchone()

    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT * FROM notification");
            data=cursor.fetchall()


            return(render(request,'notification.html',{user:'user','data':data,'rowv':rowv}))
        except:
            return(render(request,'notification.html',{user:'user','Invaliderror':'No display','rowv':rowv}))

def depview(request):
    user=request.user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM flatowner where username=%s",[request.user])
        rowv=cursor.fetchone()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM department")
        data=cursor.fetchall()
    return(render(request,'depview.html',{user:'user','data':data,'rowv':rowv}))


def maintenance(request):
    user=request.user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM flatowner where username=%s",[request.user])
        rowv=cursor.fetchone()

    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT * FROM maintenance where payeeuser=%s",[user]);
            data=cursor.fetchall()
            return(render(request,'maintenance.html',{user:'user','data':data,'rowv':rowv}))


        except:
            return(render(request,'maintenance.html',{user:'user','Invaliderror':'No display','rowv':rowv}))

def complaintregister(request):
    user=request.user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM flatowner where username=%s",[request.user])
        rowv=cursor.fetchone()
    with connection.cursor() as cursor:
        cursor.execute("SELECT dep_name FROM department")
        row=cursor.fetchall()
    if request.method == 'POST':

        complaint_des=request.POST['complaint_des']
        complaint_date=str(datetime.date.today())
        complaint_department=request.POST['dep']
        print complaint_department
        print complaint_des
        if complaint_des=="" or complaint_department is None:
            return(render(request,'complaint.html',{user:'user','Invalidrror':'Not saved','row':row,'rowv':rowv}))


        with connection.cursor() as cursor:
            try:

                cursor.execute("""INSERT INTO complaint(complaint_date,complaint_des,complainer,department) VALUES('%s','%s','%s','%s')""" %(complaint_date,complaint_des,user,complaint_department))
                return(render(request,'saved.html',{user:'user','newsaved':'saved','rowv':rowv}))
            except:
                return(render(request,'complaint.html',{user:'user','row':row,'Invalidrror':'Not saved','rowv':rowv}))
    return(render(request,'complaint.html',{user:'user','row':row,'rowv':rowv}))
def viewcomplaints(request):
    user=request.user
    print user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM flatowner where username=%s",[request.user])
        rowv=cursor.fetchone()
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT * FROM complaint WHERE complainer=%s",[user])
            data=cursor.fetchall()


            return(render(request,'complaintview.html',{user:'user','data':data,'rowv':rowv}))
        except:
            return(render(request,'complaintview.html',{user:'user','Invaliderror':'No display','rowv':rowv}))
