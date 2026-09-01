from django.contrib import admin
from django.contrib.auth.models import User
from .models import Device, Ticket

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('owner', 'brand', 'model', 'serial_number')
    search_fields = ('owner__username', 'brand', 'model', 'serial_number')
    list_filter = ('brand',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'customer', 'technician', 'created_at', 'expected_close_date')
    list_filter = ('status', 'priority', 'technician')
    search_fields = ('title', 'description', 'customer__username', 'technician__username')

