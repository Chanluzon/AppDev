from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard_user/', views.dashboard_user, name='dashboard_user'),
    path('ticket/<int:ticket_id>/', views.view_ticket, name='view_ticket'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('assigned_to_me/', views.assigned_to_me, name='assigned_to_me'),
    path('message_ticket_creator/<int:ticket_id>/', views.message_ticket_creator, name='message_ticket_creator'),  # Include the correct view name here
    path('message_ticket_user/<int:ticket_id>/', views.message_ticket_user, name='message_ticket_user'),
    path('update_ticket_status/<int:ticket_id>/', views.update_ticket_status, name='update_ticket_status'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
