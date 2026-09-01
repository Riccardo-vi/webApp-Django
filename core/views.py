from django.shortcuts import render, redirect
from django.views.generic import DeleteView, ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Ticket, Device
from .forms import TicketForm
from django.contrib.auth import logout
from django.shortcuts import redirect


def home(request):
    visits = request.session.get('visits', 0) + 1
    request.session['visits'] = visits
    latest_tickets = Ticket.objects.all()[:5]
    return render(request, 'core/home.html', {'latest_tickets': latest_tickets, 'visits': visits})

@method_decorator(login_required, name='dispatch')
class TicketListView(ListView):
    model = Ticket
    template_name = 'core/ticket_list.html'
    context_object_name = 'tickets'
    paginate_by = 5  

    def get_queryset(self):
        user = self.request.user

        # Filtraggio base in base al ruolo
        if user.groups.filter(name="Manager").exists():
            qs = Ticket.objects.all()
        elif user.groups.filter(name="Technician").exists():
            qs = Ticket.objects.filter(technician=user)
        else:
            # Customer
            qs = Ticket.objects.filter(customer=user)

        # Ricerca
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(device__brand__icontains=q) |
                Q(device__model__icontains=q)
            )

        # Filtro per stato
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)

        return qs


@method_decorator(login_required, name='dispatch')
class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'core/ticket_detail.html'

    def get_object(self, queryset=None):
        ticket = super().get_object(queryset)
        user = self.request.user

        # Manager → può vedere tutto
        if user.groups.filter(name="Manager").exists():
            return ticket

        # Technician → può vedere solo i ticket assegnati a lui
        if user.groups.filter(name="Technician").exists():
            if ticket.technician == user:
                return ticket
            raise PermissionDenied

        # Customer → può vedere solo i suoi ticket
        if ticket.customer == user:
            return ticket

        raise PermissionDenied


def toggle_theme(request):
    current = request.session.get('theme', 'light')
    request.session['theme'] = 'dark' if current == 'light' else 'light'
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@method_decorator(login_required, name='dispatch')
class MyTicketsView(ListView):
    model = Ticket
    template_name = 'core/my_tickets.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        return Ticket.objects.filter(customer=self.request.user).select_related('device')

@method_decorator(permission_required('core.add_ticket', raise_exception=True), name='dispatch')
class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'core/ticket_form.html'
    success_url = reverse_lazy('my_tickets')

    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@method_decorator(permission_required('core.change_ticket', raise_exception=True), name='dispatch')
class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'core/ticket_form.html'
    success_url = reverse_lazy('ticket_list')

    def get_object(self, queryset=None):
        ticket = super().get_object(queryset)
        user = self.request.user

        # Manager → può modificare tutto
        if user.groups.filter(name="Manager").exists():
            return ticket

        # Technician → può modificare solo i ticket assegnati a lui
        if user.groups.filter(name="Technician").exists():
            if ticket.technician == user:
                return ticket
            raise PermissionDenied

        # Customer → non può modificare nulla
        raise PermissionDenied



class DeviceListView(LoginRequiredMixin, ListView):
    model = Device
    template_name = 'core/device_list.html'

    def get_queryset(self):
        if self.request.user.groups.filter(name="Manager").exists():
            return Device.objects.all()
        return Device.objects.filter(owner=self.request.user)

class DeviceDetailView(LoginRequiredMixin, DetailView):
    model = Device
    template_name = 'core/device_detail.html'

class DeviceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Device
    fields = ['brand', 'model', 'serial_number']
    template_name = 'core/device_form.html'
    permission_required = 'core.add_device'
    success_url = reverse_lazy('device_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DeviceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Device
    fields = ['brand', 'model', 'serial_number']
    template_name = 'core/device_form.html'
    permission_required = 'core.change_device'
    success_url = reverse_lazy('device_list')

class DeviceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Device
    template_name = 'core/device_confirm_delete.html'
    permission_required = 'core.delete_device'
    success_url = reverse_lazy('device_list')


@login_required
def manager_dashboard(request):
    if not request.user.groups.filter(name="Manager").exists():
        raise PermissionDenied("Non sei manager.")
    tickets = Ticket.objects.all()
    return render(request, 'core/manager_dashboard.html', {'tickets': tickets})


def logout_view(request):
    logout(request)
    return redirect('home')
