"""
URL configuration for school_ko_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
from logic.views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', user_login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('academics/', academics, name='academics'),
    path('calendar/' ,calendar, name='calendar'),
    path('month_data/<int:month_id>/', month_data, name='month_data'),
    path('contact/', contact, name='contact'),
    path('gallery/', gallery, name='gallery'),
    path('committee/', committee, name='committee'),
    path('results/', results, name='results'),
    path('verify_user/',verify_user, name='verify_user'),
    path('logout/', logoutt, name='logout'),
    path('edit_about/', edit_about, name='edit_about'),
    path('edit_academics/', edit_academics, name='edit_academics'),
    path('send_email/', send_email, name='send_mail'),
    path('edit_contact/', edit_contact, name='edit_contact'),
    path('edit_results/', edit_results, name='edit_results'),
    path('show_events/', show_events, name='show_events'),
    path('add_event/', add_event, name='add_event'),
    path('edit_event/<int:event_id>/', edit_event, name='edit_event'),
    path('delete_event/<int:event_id>/', delete_event, name='delete_event'),
    path('edit_calender/', show_calenders, name='show_calenders'),
    path('show_calender/<int:month_id>', show_calender, name='show_calender'),
    path('update_month/', update_month, name='update_month'),
    path('show_committees/', show_committees, name='show_committees'),
    path('add_committee/', add_committee, name='add_committee'),
    path('add_member_pictures/<int:committee_id>/', add_member_pictures, name='add_member_pictures'),
    path('edit_committee/<name>/', edit_committee, name='edit_committee'),
    path('edit_member_pictures/<int:committee_id>/', edit_member_pictures, name='edit_member_pictures'),
    path('delete_committee/<name>/', delete_committee, name='delete_committee'),

]
