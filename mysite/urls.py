"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from apart import views
import apart

urlpatterns = [

    url(r'^admin/', admin.site.urls),

    

    url(r'^$',views.home,name='home'),
    url(r'^logoutuser/',views.logoutuser,name='logoutuser'),
    url(r'^loginuser/',views.loginuser,name='loginuser'),
    url(r'^ad/',views.adminlog,name="adm"),
    url(r'^adlogout/',views.adminlogout,name="admout"),
    url(r'^adduser/',views.adduser,name="adduser"),
    url(r'^addmaintenance/',views.addmaintenance,name="addmaintenance"),
    url(r'^adnotification/',views.adnotification,name="adnotification"),
    url(r'^adprofileview/',views.adprofileview,name="adprofileview"),
    url(r'^depmanager/',views.depmanager,name="depmanager"),
    url(r'^adviewcomplaints/',views.adviewcomplain,name="advcomplain"),
    url(r'^view/',views.profileview,name="profile"),
    url(r'^profile/',views.profileupdate,name="profileupdate"),
    url(r'^viewcomplaints/',views.viewcomplaints,name="viewc"),
    url(r'^complaintsregister/',views.complaintregister,name="registerc"),
    url(r'^notifications/',views.notifications,name="noti"),
    url(r'^Maintenance/',views.maintenance,name="maintain"),
    url(r'^clubs/',views.clubs,name="clubs"),
    url(r'^tenant/',views.tenant,name="tenant"),
    url(r'^change_password/',views.change_password,name="change_password"),
    url(r'^adchange_password/',views.adchange_password,name="adchange_password"),
    url(r'^clubcancel/',views.clubcancel,name="clubcancel"),
    url(r'^club_events/',views.club_events,name="club_events"),
    url(r'^deletenotification/',views.deletenotification,name="deletenotification"),
    url(r'^delevents/',views.delevents,name="delevents"),
    url(r'^tenantview/',views.tenantview,name="tenantview"),
    url(r'^depview/',views.depview,name="depview"),
    url(r'^deltenant/',views.deltenant,name="deltenant"),







]
