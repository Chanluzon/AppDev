from django.contrib import admin
from .models import TicketCategory, TicketPriority, TicketStatus, SupportTeam, SupportTicket, Message

admin.site.register(TicketCategory)
admin.site.register(TicketPriority)
admin.site.register(TicketStatus)
admin.site.register(SupportTeam)
admin.site.register(SupportTicket)
admin.site.register(Message)
