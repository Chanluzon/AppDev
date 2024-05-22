from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class TicketCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class TicketPriority(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class TicketStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SupportTeam(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(TicketCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class SupportTicket(models.Model):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    ELECTRICAL = 'Electrical'
    IT = 'IT'
    FACILITIES = 'Facilities'
    OTHER = 'Other'
    CATEGORY_CHOICES = [
        (ELECTRICAL, 'Electrical'),
        (IT, 'IT'),
        (FACILITIES, 'Facilities'),
        (OTHER, 'Other'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('Open', 'Open'),
        ('InProgress', 'InProgress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ])
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=LOW)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=OTHER)
    created_by = models.ForeignKey(User, related_name='tickets_created', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, related_name='tickets_assigned', on_delete=models.SET_NULL, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    ticket = models.ForeignKey(SupportTicket, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} on {self.timestamp}"