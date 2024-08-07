from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import SupportTicket, TicketCategory, TicketPriority, TicketStatus, Message
from django.contrib.auth.models import User
from .forms import TicketForm, MessageForm, LoginForm, MessageAndStatusForm
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.http import JsonResponse


def index(request):
    return render(request, 'support/index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            login(request, user)
            return redirect('login')  # Redirect to dashboard or any other page after successful registration
    return render(request, 'support/register.html')

@login_required
def dashboard(request):
    if request.user.is_superuser:
        tickets = SupportTicket.objects.all()
    else:
        return redirect('dashboard_user')
    
    return render(request, 'support/dashboard.html', {'tickets': tickets})

@login_required
def dashboard_user(request):
    if request.user.is_superuser:
        tickets = SupportTicket.objects.all()
    else:
        tickets = SupportTicket.objects.filter(Q(created_by=request.user) | Q(assigned_to=request.user))

    return render(request, 'support/dashboard_user.html', {'tickets': tickets})

@login_required
def view_ticket(request, ticket_id):
    if not request.user.is_superuser:
        return redirect('dashboard_user')
    
    ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id)
    user = User.objects.filter(is_superuser=False)
    has_users = user.exists()
    form = MessageForm()

    if request.method == 'POST':
        if 'assign_agent' in request.POST:
            agent_id = request.POST.get('agent')
            if agent_id:  # Ensure agent_id is not None or empty
                agent = get_object_or_404(User, id=agent_id)
                ticket.assigned_to = agent
                ticket.save()
                messages.success(request, f'Ticket assigned to {agent.username}.')
                return redirect('dashboard')
        else:
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.ticket = ticket
                message.sender = request.user
                message.save()
                return redirect('view_ticket', ticket_id=ticket_id)

    return render(request, 'support/view_ticket.html', {
        'ticket': ticket,
        'form': form,
        'users': user,
        'has_users': has_users
    })


def user_login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.has_perm('support.view_staff_status'):
                return redirect('dashboard')
            else:
                return redirect('dashboard_user')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        if request.method == 'POST':
            messages.error(request, 'Invalid form data.')
    return render(request, 'support/login.html', {'form': form})

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            return redirect('dashboard')
    else:
        form = TicketForm()
    return render(request, 'support/create_ticket.html', {'form': form})
    
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def message_ticket_creator(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id)
    if request.method == 'POST':
        form = MessageAndStatusForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.ticket = ticket
            message.sender = request.user
            message.save()
            messages.success(request, 'Message sent successfully.')
            return redirect('message_ticket_creator', ticket_id=ticket_id)
    else:
        form = MessageAndStatusForm()

    return render(request, 'support/ticketmessage.html', {
        'ticket': ticket,
        'form': form,
    })

@login_required
def message_ticket_user(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.ticket = ticket
            message.sender = request.user
            message.save()
            return redirect('message_ticket_user', ticket_id=ticket.id)
    else:
        form = MessageForm()
    return render(request, 'support/ticketmessage_user.html', {'ticket': ticket, 'form': form})

@login_required
def assigned_to_me(request):
    assigned_to_me_tickets = SupportTicket.objects.filter(assigned_to=request.user)
    return render(request, 'support/assigned_to_me.html', {'assigned_to_me_tickets': assigned_to_me_tickets})

@login_required
def update_ticket_status(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Open','Resolved', 'Closed', 'InProgress']:
            ticket.status = new_status
            ticket.save()
            messages.success(request, f'Ticket has been {new_status.lower()}.')

            # Send notifications to both the admin and the ticket creator
            #if ticket.assigned_to:
                #create_notification_message(ticket, new_status, request.user)

    return redirect('message_ticket_creator', ticket_id=ticket_id)

def delete_tickets(request):
    if request.method == 'POST':
        ticket_ids = request.POST.getlist('ticket_id')
        try:
            tickets_to_delete = SupportTicket.objects.filter(ticket_id__in=ticket_ids)
            tickets_to_delete.delete()
            return redirect('dashboard')  # Redirect to dashboard view on success
        except SupportTicket.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Tickets not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

@login_required
def assigned_to_me(request):
    assigned_to_me_tickets = SupportTicket.objects.filter(assigned_to=request.user)
    return render(request, 'support/assigned_to_me.html', {'assigned_to_me_tickets': assigned_to_me_tickets})

@login_required
def update_ticket_status(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Open','Resolved', 'Closed', 'InProgress']:
            ticket.status = new_status
            ticket.save()
            messages.success(request, f'Ticket has been {new_status.lower()}.')

            # Send notifications to both the admin and the ticket creator
            #if ticket.assigned_to:
                #create_notification_message(ticket, new_status, request.user)

    return redirect('message_ticket_creator', ticket_id=ticket_id)

def delete_tickets(request):
    if request.method == 'POST':
        ticket_ids = request.POST.getlist('ticket_id')
        try:
            tickets_to_delete = SupportTicket.objects.filter(ticket_id__in=ticket_ids)
            tickets_to_delete.delete()
            return redirect('dashboard')  # Redirect to dashboard view on success
        except SupportTicket.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Tickets not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

@login_required
def open_tickets(request):
    if request.user.is_superuser:
        open_tickets = SupportTicket.objects.filter(status='Open')
    else:
        open_tickets = SupportTicket.objects.filter(status='Open', assigned_to=request.user)
    return render(request, 'support/open_tickets.html', {'tickets': open_tickets})

@login_required
def in_progress_tickets(request):
    if request.user.is_superuser:
        in_progress_tickets = SupportTicket.objects.filter(status='InProgress')
    else:
        in_progress_tickets = SupportTicket.objects.filter(status='InProgress', assigned_to=request.user)
    return render(request, 'support/pending_tickets.html', {'tickets': in_progress_tickets})

@login_required
def resolved_tickets(request):
    if request.user.is_superuser:
        resolved_tickets = SupportTicket.objects.filter(status='Resolved')
    else:
        resolved_tickets = SupportTicket.objects.filter(status='Resolved', assigned_to=request.user)
    return render(request, 'support/resolved_tickets.html', {'tickets': resolved_tickets})

@login_required
def closed_tickets(request):
    if request.user.is_superuser:
        closed_tickets = SupportTicket.objects.filter(status='Closed')
    else:
        closed_tickets = SupportTicket.objects.filter(status='Closed', assigned_to=request.user)
    return render(request, 'support/closed_tickets.html', {'tickets': closed_tickets})

@login_required
def unassigned_tickets(request):
    if request.user.is_superuser:
        unassigned_tickets = SupportTicket.objects.filter(assigned_to__isnull=True)
    else:
        unassigned_tickets = SupportTicket.objects.filter(assigned_to__isnull=True, created_by=request.user)
    return render(request, 'support/unassigned_tickets.html', {'tickets': unassigned_tickets})

@login_required
def search_tickets(request):
    query = request.GET.get('q', '')
    if request.user.is_superuser:
        tickets = SupportTicket.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        tickets = SupportTicket.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            Q(created_by=request.user) | Q(assigned_to=request.user)
        )
    return render(request, 'support/search_results.html', {'tickets': tickets})